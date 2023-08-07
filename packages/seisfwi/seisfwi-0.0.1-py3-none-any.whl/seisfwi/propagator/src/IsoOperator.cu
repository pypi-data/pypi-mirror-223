#include "Boundary.h"
#include "Cpml.h"
#include "Model.h"
#include "Parameter.h"
#include "Survey.h"
#include "utils.h"
#include <chrono>
#include <string>
using std::string;


extern "C" void Propagator(const string para_fname, const int gpu_id,
                           const int group_size, const int *shot_ids,
                           const float *Lambda, const float *Mu,
                           const float *Den, const float *stf,
                           const bool is_acoustic, const bool with_adj) {

  // Set GPU device
  CHECK(cudaSetDevice(gpu_id));
  auto start0 = std::chrono::high_resolution_clock::now();

  // Read parameter file
  Parameter para(para_fname);
  int nz = para.nz();
  int nx = para.nx();
  int nt = para.nt();
  int npml = para.npml();
  int npad = para.npad();
  float dx = para.dx();
  float dz = para.dz();
  float dt = para.dt();
  float f0 = para.f0();
  float weight_pr = para.weight_pr();
  float weight_vx = para.weight_vx();
  float weight_vz = para.weight_vz();
  float weight_et = para.weight_et();

  // Set default values
  int nrec = 1;
  int ndas = 1;

  // Transpose models and convert to float
  float *fLambda, *fMu, *fDen;
  fLambda = (float *)malloc(nz * nx * sizeof(float));
  fMu = (float *)malloc(nz * nx * sizeof(float));
  fDen = (float *)malloc(nz * nx * sizeof(float));
  for (int i = 0; i < nz; i++) {
    for (int j = 0; j < nx; j++) {
      fLambda[j * nz + i] = Lambda[i * nx + j] * MEGA;
      fMu[j * nz + i] = Mu[i * nx + j] * MEGA;
      fDen[j * nz + i] = Den[i * nx + j];
    }
  }

  // Set up model
  Model model(para, fLambda, fMu, fDen);

  // Set up CPML boundary conditions
  Cpml cpml(para, model);

  // Set up source and receiver
  bool with_residual = false;
  Survey survey(para, with_adj, with_residual, stf, group_size, shot_ids);

  // Compute Courant number
  compCourantNumber(model.h_Vp, nz * nx, dt, dz, dx);

  // Set up GPU threads and blocks
  dim3 threads(TX, TY);
  dim3 blocks((nz + TX - 1) / TX, (nx + TY - 1) / TY);

  // Define device memory
  float *d_vz, *d_vx, *d_szz, *d_sxx, *d_sxz;
  float *d_mem_dvz_dz, *d_mem_dvz_dx, *d_mem_dvx_dz, *d_mem_dvx_dx;
  float *d_mem_dszz_dz, *d_mem_dsxx_dx, *d_mem_dsxz_dz, *d_mem_dsxz_dx;
  float *d_gauss_amp;

  float *d_syn_pr; // pressure data
  float *d_syn_vx; // vertical velocity data
  float *d_syn_vz; // horizontal velocity data
  float *d_syn_et; // tangential strain data
  float *d_adj_pr; // pressure, as I use explosive source

  // Allocate device memory: forward wavefield
  CHECK(cudaMalloc((void **)&d_vz, nz * nx * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_vx, nz * nx * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_szz, nz * nx * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_sxx, nz * nx * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_sxz, nz * nx * sizeof(float)));

  // Allocate device memory: memory variables for PML
  CHECK(cudaMalloc((void **)&d_mem_dvz_dz, nz * nx * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_mem_dvz_dx, nz * nx * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_mem_dvx_dz, nz * nx * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_mem_dvx_dx, nz * nx * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_mem_dszz_dz, nz * nx * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_mem_dsxx_dx, nz * nx * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_mem_dsxz_dz, nz * nx * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_mem_dsxz_dx, nz * nx * sizeof(float)));

  // Set the source gaussian amplitude
  CHECK(cudaMalloc((void **)&d_gauss_amp, 81 * sizeof(float)));
  src_rec_gauss_amp<<<1, threads>>>(d_gauss_amp, 9, 9);

  // float *h_snap;
  // h_snap = (float *)malloc(nz * nx * sizeof(float));

  // Start the stream
  cudaStream_t streams[group_size];

  // Modeling over shots
  for (int iShot = 0; iShot < group_size; iShot++) {
    // printf("  Processing shot %d\n", shot_ids[iShot]);

    // Set up the source
    CHECK(cudaStreamCreate(&streams[iShot]));

    // Initialize the wavefields
    intialArrayGPU<<<blocks, threads>>>(d_vz, nz, nx, 0.0);
    intialArrayGPU<<<blocks, threads>>>(d_vx, nz, nx, 0.0);
    intialArrayGPU<<<blocks, threads>>>(d_szz, nz, nx, 0.0);
    intialArrayGPU<<<blocks, threads>>>(d_sxx, nz, nx, 0.0);
    intialArrayGPU<<<blocks, threads>>>(d_sxz, nz, nx, 0.0);

    intialArrayGPU<<<blocks, threads>>>(d_mem_dvz_dz, nz, nx, 0.0);
    intialArrayGPU<<<blocks, threads>>>(d_mem_dvz_dx, nz, nx, 0.0);
    intialArrayGPU<<<blocks, threads>>>(d_mem_dvx_dz, nz, nx, 0.0);
    intialArrayGPU<<<blocks, threads>>>(d_mem_dvx_dx, nz, nx, 0.0);
    intialArrayGPU<<<blocks, threads>>>(d_mem_dszz_dz, nz, nx, 0.0);
    intialArrayGPU<<<blocks, threads>>>(d_mem_dsxx_dx, nz, nx, 0.0);
    intialArrayGPU<<<blocks, threads>>>(d_mem_dsxz_dz, nz, nx, 0.0);
    intialArrayGPU<<<blocks, threads>>>(d_mem_dsxz_dx, nz, nx, 0.0);

    // Read the receiver data
    nrec = survey.vec_nrec.at(iShot);
    ndas = survey.vec_ndas.at(iShot);

    // Allocate device memory for syn data and intialize to zero
    CHECK(cudaMalloc((void **)&d_syn_pr, nrec * nt * sizeof(float)));
    CHECK(cudaMalloc((void **)&d_syn_vx, nrec * nt * sizeof(float)));
    CHECK(cudaMalloc((void **)&d_syn_vz, nrec * nt * sizeof(float)));
    CHECK(cudaMalloc((void **)&d_syn_et, ndas * nt * sizeof(float)));
    intialArrayGPU<<<blocks, threads>>>(d_syn_pr, nt, nrec, 0.0);
    intialArrayGPU<<<blocks, threads>>>(d_syn_vx, nt, nrec, 0.0);
    intialArrayGPU<<<blocks, threads>>>(d_syn_vz, nt, nrec, 0.0);
    intialArrayGPU<<<blocks, threads>>>(d_syn_et, nt, ndas, 0.0);

    // ------------------------ forward time loop (elastic) ----------------------------
    if (is_acoustic) {

      // std::cout << "Forward modeling: acoustic" << std::endl;

      for (int it = 0; it <= nt - 2; it++) {
        // Update the stress
        acoustic_forward_pressure<<<blocks, threads>>>(
            d_vz, d_vx, d_szz, d_mem_dvz_dz, d_mem_dvx_dx, model.d_Lambda,
            cpml.d_K_z_half, cpml.d_a_z_half, cpml.d_b_z_half, cpml.d_K_x,
            cpml.d_a_x, cpml.d_b_x, nz, nx, dt, dz, dx, npml, npad);

        // Add explosive source
        add_source<<<1, 1>>>(d_szz, d_sxx, survey.vec_source.at(iShot)[it], nz,
                             survey.vec_z_src.at(iShot),
                             survey.vec_x_src.at(iShot), dt, d_gauss_amp);

        // Update the velocity
        acoustic_forward_velocity<<<blocks, threads>>>(
            d_vz, d_vx, d_szz, d_mem_dszz_dz, d_mem_dsxx_dx, model.d_ave_Byc_a,
            model.d_ave_Byc_b, cpml.d_K_z, cpml.d_a_z, cpml.d_b_z,
            cpml.d_K_x_half, cpml.d_a_x_half, cpml.d_b_x_half, nz, nx, dt, dz,
            dx, npml, npad);

        // Record syn data recored by geophone: pr = sxx + szz, vx, vz
        record_geo<<<(nrec + 31) / 32, 32>>>(
            d_szz, d_sxx, d_vx, d_vz, nz, d_syn_pr, d_syn_vx, d_syn_vz,
            iShot, it + 1, nt, nrec, survey.d_vec_z_rec.at(iShot),
            survey.d_vec_x_rec.at(iShot));

        // Record syn data recored by DAS: et
        record_das<<<(ndas + 31) / 32, 32>>>(
          d_vx, d_vz, nz, d_syn_et,
          iShot, it + 1, nt, ndas, survey.d_vec_z_das.at(iShot),
          survey.d_vec_x_das.at(iShot), survey.d_vec_das_wt_x.at(iShot), 
          survey.d_vec_das_wt_z.at(iShot), survey.gl);
      }
    } else {
      // std::cout << "Forward modeling: elastic" << std::endl;
      for (int it = 0; it <= nt - 2; it++) {

        // Update stress
        elastic_forward_stress<<<blocks, threads>>>(
            d_vz, d_vx, d_szz, d_sxx, d_sxz, d_mem_dvz_dz, d_mem_dvz_dx,
            d_mem_dvx_dz, d_mem_dvx_dx, model.d_Lambda, model.d_Mu,
            model.d_ave_Mu, cpml.d_K_z, cpml.d_a_z, cpml.d_b_z, cpml.d_K_z_half,
            cpml.d_a_z_half, cpml.d_b_z_half, cpml.d_K_x, cpml.d_a_x,
            cpml.d_b_x, cpml.d_K_x_half, cpml.d_a_x_half, cpml.d_b_x_half, nz,
            nx, dt, dz, dx, npml, npad);

        // Add explosive source
        add_source<<<1, threads>>>(d_szz, d_sxx,
                                   survey.vec_source.at(iShot)[it], nz,
                                   survey.vec_z_src.at(iShot),
                                   survey.vec_x_src.at(iShot), dt, d_gauss_amp);

        // Update velocity
        elastic_forward_velocity<<<blocks, threads>>>(
            d_vz, d_vx, d_szz, d_sxx, d_sxz, d_mem_dszz_dz, d_mem_dsxz_dx,
            d_mem_dsxz_dz, d_mem_dsxx_dx, model.d_ave_Byc_a, model.d_ave_Byc_b,
            cpml.d_K_z, cpml.d_a_z, cpml.d_b_z, cpml.d_K_z_half,
            cpml.d_a_z_half, cpml.d_b_z_half, cpml.d_K_x, cpml.d_a_x,
            cpml.d_b_x, cpml.d_K_x_half, cpml.d_a_x_half, cpml.d_b_x_half, nz,
            nx, dt, dz, dx, npml, npad);

        // Record syn data recored by geophone: pr = sxx + szz, vx, vz
        record_geo<<<(nrec + 31) / 32, 32>>>(
            d_szz, d_sxx, d_vx, d_vz, nz, d_syn_pr, d_syn_vx, d_syn_vz,
            iShot, it + 1, nt, nrec, survey.d_vec_z_rec.at(iShot),
            survey.d_vec_x_rec.at(iShot));
        
        // Record syn data recored by DAS: et
        record_das<<<(ndas + 31) / 32, 32>>>(
          d_vx, d_vz, nz, d_syn_et,
          iShot, it + 1, nt, ndas, survey.d_vec_z_das.at(iShot),
          survey.d_vec_x_das.at(iShot), survey.d_vec_das_wt_x.at(iShot), 
          survey.d_vec_das_wt_z.at(iShot), survey.gl);

        // // Save wavefield for debug
        // if (iShot == 0 && it % 100 == 0) {
        //   CHECK(cudaMemcpy(h_snap, d_szz, nz * nx * sizeof(float), cudaMemcpyDeviceToHost));
        //   fileBinWrite(h_snap, nz * nx, "SnapGPU_" + std::to_string(it) + ".bin");
        // }

      } // end of forward time loop
    }
    // Copy data back to host memory, only for forward modeling
    CHECK(cudaMemcpyAsync(survey.vec_syn_pr.at(iShot), d_syn_pr,
                          nt * nrec * sizeof(float), cudaMemcpyDeviceToHost,
                          streams[iShot]));
    CHECK(cudaMemcpyAsync(survey.vec_syn_vx.at(iShot), d_syn_vx,
                          nt * nrec * sizeof(float), cudaMemcpyDeviceToHost,
                          streams[iShot]));
    CHECK(cudaMemcpyAsync(survey.vec_syn_vz.at(iShot), d_syn_vz,
                          nt * nrec * sizeof(float), cudaMemcpyDeviceToHost,
                          streams[iShot]));
    CHECK(cudaMemcpyAsync(survey.vec_syn_et.at(iShot), d_syn_et,
                          nt * ndas * sizeof(float), cudaMemcpyDeviceToHost,
                          streams[iShot]));

    // synchronize all streams
    cudaDeviceSynchronize();

    if (with_adj) {
      // Allocate device memory for adj data and intialize to zero
      CHECK(cudaMalloc((void **)&d_adj_pr, 1 * nt * sizeof(float)));
      intialArrayGPU<<<blocks, threads>>>(d_adj_pr, nt, 1, 0.0);

      //  Initialize the wavefields
      intialArrayGPU<<<blocks, threads>>>(d_vz, nz, nx, 0.0);
      intialArrayGPU<<<blocks, threads>>>(d_vx, nz, nx, 0.0);
      intialArrayGPU<<<blocks, threads>>>(d_szz, nz, nx, 0.0);
      intialArrayGPU<<<blocks, threads>>>(d_sxx, nz, nx, 0.0);
      intialArrayGPU<<<blocks, threads>>>(d_sxz, nz, nx, 0.0);

      intialArrayGPU<<<blocks, threads>>>(d_mem_dvz_dz, nz, nx, 0.0);
      intialArrayGPU<<<blocks, threads>>>(d_mem_dvz_dx, nz, nx, 0.0);
      intialArrayGPU<<<blocks, threads>>>(d_mem_dvx_dz, nz, nx, 0.0);
      intialArrayGPU<<<blocks, threads>>>(d_mem_dvx_dx, nz, nx, 0.0);
      intialArrayGPU<<<blocks, threads>>>(d_mem_dszz_dz, nz, nx, 0.0);
      intialArrayGPU<<<blocks, threads>>>(d_mem_dsxx_dx, nz, nx, 0.0);
      intialArrayGPU<<<blocks, threads>>>(d_mem_dsxz_dz, nz, nx, 0.0);
      intialArrayGPU<<<blocks, threads>>>(d_mem_dsxz_dx, nz, nx, 0.0);

      if (is_acoustic) {
        // std::cout << "Adjoint modeling: acoustic" << std::endl;
        for (int it = nt - 2; it >= 0; it--) {
          // update velocity of the adjoint wavefield
          acoustic_adjoint_velocity<<<blocks, threads>>>(
              d_vz, d_vx, d_szz, d_mem_dvz_dz, d_mem_dvx_dx, d_mem_dszz_dz,
              d_mem_dsxx_dx, model.d_Lambda, model.d_ave_Byc_a,
              model.d_ave_Byc_b, cpml.d_K_z_half, cpml.d_a_z_half,
              cpml.d_b_z_half, cpml.d_K_x_half, cpml.d_a_x_half,
              cpml.d_b_x_half, cpml.d_K_z, cpml.d_a_z, cpml.d_b_z, cpml.d_K_x,
              cpml.d_a_x, cpml.d_b_x, nz, nx, dt, dz, dx, npml, npad);

          // record pressure data
          record_adj<<<(nrec + 31) / 32, 32>>>(
              d_szz, d_sxx, nz, d_adj_pr, iShot, it, nt, 1,
              survey.vec_z_src.at(iShot), survey.vec_x_src.at(iShot));

          // inject geophone residuals
          inject_geo<<<(nrec + 31) / 32, 32>>>(
            d_szz, d_sxx, d_vx, d_vz, nz, d_syn_pr, d_syn_vx,
            d_syn_vz, it, dt, nt, nrec, survey.d_vec_z_rec.at(iShot), 
            survey.d_vec_x_rec.at(iShot), weight_pr, weight_vx, weight_vz);
        
          // inject das residuals
          inject_das<<<(ndas + 31) / 32, 32>>>(d_vx, d_vz, nz, d_syn_et, 
              it, dt, nt, ndas, survey.d_vec_z_das.at(iShot), 
              survey.d_vec_x_das.at(iShot), weight_et, 
              survey.d_vec_das_wt_x.at(iShot), 
              survey.d_vec_das_wt_z.at(iShot), survey.gl);

          // update stress of the adjoint wavefield
          acoustic_adjoint_pressure<<<blocks, threads>>>(
              d_vz, d_vx, d_szz, d_mem_dvz_dz, d_mem_dvx_dx, d_mem_dszz_dz,
              d_mem_dsxx_dx, model.d_Lambda, model.d_ave_Byc_a,
              model.d_ave_Byc_b, cpml.d_K_z_half, cpml.d_a_z_half,
              cpml.d_b_z_half, cpml.d_K_x_half, cpml.d_a_x_half,
              cpml.d_b_x_half, cpml.d_K_z, cpml.d_a_z, cpml.d_b_z, cpml.d_K_x,
              cpml.d_a_x, cpml.d_b_x, nz, nx, dt, dz, dx, npml, npad);
        }
      } else {
        // std::cout << "Adjoint modeling: elastic" << std::endl;
        // ----------adjoint time loop (elastic) ----------
        for (int it = nt - 2; it >= 0; it--) {

          // update velocity of the adjoint wavefield
          elastic_adjoint_velocity<<<blocks, threads>>>(
              d_vz, d_vx, d_szz, d_sxx, d_sxz, d_mem_dszz_dz, d_mem_dsxz_dx,
              d_mem_dsxz_dz, d_mem_dsxx_dx, d_mem_dvz_dz, d_mem_dvz_dx,
              d_mem_dvx_dz, d_mem_dvx_dx, model.d_Lambda, model.d_Mu,
              model.d_ave_Mu, model.d_Den, model.d_ave_Byc_a, model.d_ave_Byc_b,
              cpml.d_K_z_half, cpml.d_a_z_half, cpml.d_b_z_half,
              cpml.d_K_x_half, cpml.d_a_x_half, cpml.d_b_x_half, cpml.d_K_z,
              cpml.d_a_z, cpml.d_b_z, cpml.d_K_x, cpml.d_a_x, cpml.d_b_x, nz,
              nx, dt, dz, dx, npml, npad);

          // record pressure data
          record_adj<<<(nrec + 31) / 32, 32>>>(
              d_szz, d_sxx, nz, d_adj_pr, iShot, it, nt, 1,
              survey.vec_z_src.at(iShot), survey.vec_x_src.at(iShot));

          // inject geophone residuals
          inject_geo<<<(nrec + 31) / 32, 32>>>(
            d_szz, d_sxx, d_vx, d_vz, nz, d_syn_pr, d_syn_vx,
            d_syn_vz, it, dt, nt, nrec, survey.d_vec_z_rec.at(iShot), 
            survey.d_vec_x_rec.at(iShot), weight_pr, weight_vx, weight_vz);
        
          // inject das residuals
          inject_das<<<(ndas + 31) / 32, 32>>>(d_vx, d_vz, nz, d_syn_et, 
              it, dt, nt, ndas, survey.d_vec_z_das.at(iShot), 
              survey.d_vec_x_das.at(iShot), weight_et, 
              survey.d_vec_das_wt_x.at(iShot), 
              survey.d_vec_das_wt_z.at(iShot), survey.gl);

          // update velocity of the adjoint wavefield
          elastic_adjoint_stress<<<blocks, threads>>>(
              d_vz, d_vx, d_szz, d_sxx, d_sxz, d_mem_dszz_dz, d_mem_dsxz_dx,
              d_mem_dsxz_dz, d_mem_dsxx_dx, d_mem_dvz_dz, d_mem_dvz_dx,
              d_mem_dvx_dz, d_mem_dvx_dx, model.d_Lambda, model.d_Mu,
              model.d_ave_Mu, model.d_Den, model.d_ave_Byc_a, model.d_ave_Byc_b,
              cpml.d_K_z_half, cpml.d_a_z_half, cpml.d_b_z_half,
              cpml.d_K_x_half, cpml.d_a_x_half, cpml.d_b_x_half, cpml.d_K_z,
              cpml.d_a_z, cpml.d_b_z, cpml.d_K_x, cpml.d_a_x, cpml.d_b_x, nz,
              nx, dt, dz, dx, npml, npad);

        } // the end of backward time loop
      }

      // transfer the adjoint pressure data to cpu
      CHECK(cudaMemcpyAsync(survey.vec_adj_pr.at(iShot), d_adj_pr,
                            nt * 1 * sizeof(float), cudaMemcpyDeviceToHost,
                            streams[iShot]));

      // free the memory on device
      CHECK(cudaFree(d_adj_pr));
    }

    // free memory on GPU
    CHECK(cudaFree(d_syn_pr));
    CHECK(cudaFree(d_syn_vx));
    CHECK(cudaFree(d_syn_vz));
    CHECK(cudaFree(d_syn_et));

  } // the end of shot loop

  // save the shot record
  for (int iShot = 0; iShot < group_size; iShot++) {
    fileBinWrite(survey.vec_syn_pr.at(iShot), nt * survey.vec_nrec.at(iShot),
                 para.data_dir_name() + "/shot" +
                     std::to_string(shot_ids[iShot]) + "_pr.bin");
    fileBinWrite(survey.vec_syn_vx.at(iShot), nt * survey.vec_nrec.at(iShot),
                 para.data_dir_name() + "/shot" +
                     std::to_string(shot_ids[iShot]) + "_vx.bin");
    fileBinWrite(survey.vec_syn_vz.at(iShot), nt * survey.vec_nrec.at(iShot),
                 para.data_dir_name() + "/shot" +
                     std::to_string(shot_ids[iShot]) + "_vz.bin");
    fileBinWrite(survey.vec_syn_et.at(iShot), nt * survey.vec_ndas.at(iShot),
                 para.data_dir_name() + "/shot" +
                     std::to_string(shot_ids[iShot]) + "_et.bin");

    if (with_adj) {
      fileBinWrite(survey.vec_adj_pr.at(iShot), nt * 1,
                   para.data_dir_name() + "/adj_shot" +
                       std::to_string(shot_ids[iShot]) + "_pr.bin");
    }
  }

  free(fLambda);
  free(fMu);
  free(fDen);
  // free(h_snap);

  // destroy the streams
  for (int iShot = 0; iShot < group_size; iShot++) {
    CHECK(cudaStreamDestroy(streams[iShot]));
  }

  cudaFree(d_vz);
  cudaFree(d_vx);
  cudaFree(d_szz);
  cudaFree(d_sxx);
  cudaFree(d_sxz);
  cudaFree(d_mem_dvz_dz);
  cudaFree(d_mem_dvz_dx);
  cudaFree(d_mem_dvx_dz);
  cudaFree(d_mem_dvx_dx);
  cudaFree(d_mem_dszz_dz);
  cudaFree(d_mem_dsxx_dx);
  cudaFree(d_mem_dsxz_dz);
  cudaFree(d_mem_dsxz_dx);
  cudaFree(d_gauss_amp);
}



extern "C" void Gradient(const string para_fname, const int gpu_id,
                         const int group_size, const int *shot_ids,
                         const float *Lambda, const float *Mu, const float *Den,
                         const float *stf, float *misfit, float *grad_Lambda,
                         float *grad_Mu, float *grad_Den, float *grad_Vp,
                         float *grad_stf, const bool is_acoustic,
                         const bool with_grad) {

  // Set GPU device
  CHECK(cudaSetDevice(gpu_id));
  auto start0 = std::chrono::high_resolution_clock::now();

  // Read parameter file
  Parameter para(para_fname);
  int nz = para.nz();
  int nx = para.nx();
  int nt = para.nt();
  int npml = para.npml();
  int npad = para.npad();
  float dx = para.dx();
  float dz = para.dz();
  float dt = para.dt();
  float f0 = para.f0();
  float weight_pr = para.weight_pr();
  float weight_vx = para.weight_vx();
  float weight_vz = para.weight_vz();
  float weight_et = para.weight_et();

  // Set default values
  int nrec = 1;
  int ndas = 1;
  float win_ratio = 0.000; // 0.005
  float amp_ratio = 1.0;

  // Transpose models and convert to float
  float *fLambda, *fMu, *fDen;
  fLambda = (float *)malloc(nz * nx * sizeof(float));
  fMu = (float *)malloc(nz * nx * sizeof(float));
  fDen = (float *)malloc(nz * nx * sizeof(float));
  for (int i = 0; i < nz; i++) {
    for (int j = 0; j < nx; j++) {
      fLambda[j * nz + i] = Lambda[i * nx + j] * MEGA;
      fMu[j * nz + i] = Mu[i * nx + j] * MEGA;
      fDen[j * nz + i] = Den[i * nx + j];
    }
  }

  // Set up model
  Model model(para, fLambda, fMu, fDen);

  // Set up CPML boundary conditions
  Cpml cpml(para, model);

  // Set up boundaries for reconstruction in gradient calculation
  Bnd boundaries(para, with_grad);

  // Set up source and receiver
  bool with_adj = false;
  bool with_residual = true;
  Survey survey(para, with_adj, with_residual, stf, group_size, shot_ids);

  // Compute Courant number
  compCourantNumber(model.h_Vp, nz * nx, dt, dz, dx);

  // Set up GPU threads and blocks
  dim3 threads(TX, TY);
  dim3 blocks((nz + TX - 1) / TX, (nx + TY - 1) / TY);

  // Define device memory
  float *d_vz, *d_vx, *d_szz, *d_sxx, *d_sxz;
  float *d_vz_adj, *d_vx_adj, *d_szz_adj, *d_sxx_adj, *d_sxz_adj;
  float *d_mem_dvz_dz, *d_mem_dvz_dx, *d_mem_dvx_dz, *d_mem_dvx_dx;
  float *d_mem_dszz_dz, *d_mem_dsxx_dx, *d_mem_dsxz_dz, *d_mem_dsxz_dx;
  float *d_obj_pr, *d_obj_vx, *d_obj_vz, *d_obj_et;
  float *d_gauss_amp;
  float *h_obj_pr = nullptr;
  float *h_obj_vx = nullptr;
  float *h_obj_vz = nullptr;
  float *h_obj_et = nullptr;
  float h_obj = 0.0;

  // for acoustic
  float *d_szz_p1;

  // Synthetic data
  float *d_syn_pr; // pressure
  float *d_syn_vx; // vertical velocity
  float *d_syn_vz; // horizontal velocity
  float *d_syn_et; // tangential strain

  // Observed data
  float *d_obs_pr; // pressure
  float *d_obs_vx; // vertical velocity
  float *d_obs_vz; // horizontal velocity
  float *d_obs_et; // tangential strain

  // Residual data
  float *d_res_pr; // pressure
  float *d_res_vx; // vertical velocity
  float *d_res_vz; // horizontal velocity
  float *d_res_et; // tangential strain

  // Allocate device memory: forward wavefield
  CHECK(cudaMalloc((void **)&d_vz, nz * nx * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_vx, nz * nx * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_szz, nz * nx * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_sxx, nz * nx * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_sxz, nz * nx * sizeof(float)));

  // Allocate device memory: memory variables for computing gradient
  CHECK(cudaMalloc((void **)&d_mem_dvz_dz, nz * nx * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_mem_dvz_dx, nz * nx * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_mem_dvx_dz, nz * nx * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_mem_dvx_dx, nz * nx * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_mem_dszz_dz, nz * nx * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_mem_dsxx_dx, nz * nx * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_mem_dsxz_dz, nz * nx * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_mem_dsxz_dx, nz * nx * sizeof(float)));

  // Allocate device memory: adjoint wavefield
  CHECK(cudaMalloc((void **)&d_vz_adj, nz * nx * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_vx_adj, nz * nx * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_szz_adj, nz * nx * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_sxx_adj, nz * nx * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_sxz_adj, nz * nx * sizeof(float)));
  if (is_acoustic) {
    CHECK(cudaMalloc((void **)&d_szz_p1, nz * nx * sizeof(float)));
  }
  // Allocate device memory: objective function
  CHECK(cudaMalloc((void **)&d_obj_pr, 1 * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_obj_vx, 1 * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_obj_vz, 1 * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_obj_et, 1 * sizeof(float)));
  h_obj_pr = (float *)malloc(sizeof(float));
  h_obj_vx = (float *)malloc(sizeof(float));
  h_obj_vz = (float *)malloc(sizeof(float));
  h_obj_et = (float *)malloc(sizeof(float));

  // Set the source gaussian amplitude
  CHECK(cudaMalloc((void **)&d_gauss_amp, 81 * sizeof(float)));
  src_rec_gauss_amp<<<1, threads>>>(d_gauss_amp, 9, 9);

 // float *h_snap;
 // h_snap = (float *)malloc(nz * nx * sizeof(float));

  // Start the stream
  cudaStream_t streams[group_size];

  // Modeling over shots
  for (int iShot = 0; iShot < group_size; iShot++) {
    // printf("  Processing shot %d\n", shot_ids[iShot]);

    // Set grid and block size for residuals
    dim3 blocksT_rec((nt + TX - 1) / TX, (nrec + TY - 1) / TY);
    dim3 blocksT_das((nt + TX - 1) / TX, (ndas + TY - 1) / TY);

    // Set up the source
    CHECK(cudaStreamCreate(&streams[iShot]));

    // Read the receiver data
    nrec = survey.vec_nrec.at(iShot);
    ndas = survey.vec_ndas.at(iShot);
      
    // Load the observed data
    fileBinLoad(survey.vec_obs_pr.at(iShot), nt * nrec,
                para.data_dir_name() + "/shot" +
                    std::to_string(shot_ids[iShot]) + "_pr.bin");
    fileBinLoad(survey.vec_obs_vx.at(iShot), nt * nrec,
                para.data_dir_name() + "/shot" +
                    std::to_string(shot_ids[iShot]) + "_vx.bin");
    fileBinLoad(survey.vec_obs_vz.at(iShot), nt * nrec,
                para.data_dir_name() + "/shot" +
                    std::to_string(shot_ids[iShot]) + "_vz.bin");
    fileBinLoad(survey.vec_obs_et.at(iShot), nt * ndas,
                para.data_dir_name() + "/shot" +
                    std::to_string(shot_ids[iShot]) + "_et.bin");

    // Allocate device memory for obs data and then copy from host to device
    CHECK(cudaMalloc((void **)&d_obs_pr, nrec * nt * sizeof(float)));
    CHECK(cudaMalloc((void **)&d_obs_vx, nrec * nt * sizeof(float)));
    CHECK(cudaMalloc((void **)&d_obs_vz, nrec * nt * sizeof(float)));
    CHECK(cudaMalloc((void **)&d_obs_et, ndas * nt * sizeof(float)));

    intialArrayGPU<<<blocksT_rec, threads>>>(d_obs_pr, nt, nrec, 0.0);
    intialArrayGPU<<<blocksT_rec, threads>>>(d_obs_vx, nt, nrec, 0.0);
    intialArrayGPU<<<blocksT_rec, threads>>>(d_obs_vz, nt, nrec, 0.0);
    intialArrayGPU<<<blocksT_das, threads>>>(d_obs_et, nt, ndas, 0.0);

    CHECK(cudaMemcpyAsync(d_obs_pr, survey.vec_obs_pr.at(iShot), nrec * nt * sizeof(float), cudaMemcpyHostToDevice,
                          streams[iShot]));
    CHECK(cudaMemcpyAsync(d_obs_vx, survey.vec_obs_vx.at(iShot), nrec * nt * sizeof(float), cudaMemcpyHostToDevice,
                          streams[iShot]));
    CHECK(cudaMemcpyAsync(d_obs_vz, survey.vec_obs_vz.at(iShot), nrec * nt * sizeof(float), cudaMemcpyHostToDevice,
                          streams[iShot]));
    CHECK(cudaMemcpyAsync(d_obs_et, survey.vec_obs_et.at(iShot), ndas * nt * sizeof(float), cudaMemcpyHostToDevice,
                          streams[iShot]));

    // Allocate device memory for syn data and intialize to zero
    CHECK(cudaMalloc((void **)&d_syn_pr, nrec * nt * sizeof(float)));
    CHECK(cudaMalloc((void **)&d_syn_vx, nrec * nt * sizeof(float)));
    CHECK(cudaMalloc((void **)&d_syn_vz, nrec * nt * sizeof(float)));
    CHECK(cudaMalloc((void **)&d_syn_et, ndas * nt * sizeof(float)));

    intialArrayGPU<<<blocksT_rec, threads>>>(d_syn_pr, nt, nrec, 0.0);
    intialArrayGPU<<<blocksT_rec, threads>>>(d_syn_vx, nt, nrec, 0.0);
    intialArrayGPU<<<blocksT_rec, threads>>>(d_syn_vz, nt, nrec, 0.0);
    intialArrayGPU<<<blocksT_das, threads>>>(d_syn_et, nt, ndas, 0.0);

    // Allocate device memory for res data and initialize to zero
    CHECK(cudaMalloc((void **)&d_res_pr, nrec * nt * sizeof(float)));
    CHECK(cudaMalloc((void **)&d_res_vx, nrec * nt * sizeof(float)));
    CHECK(cudaMalloc((void **)&d_res_vz, nrec * nt * sizeof(float)));
    CHECK(cudaMalloc((void **)&d_res_et, ndas * nt * sizeof(float)));

    intialArrayGPU<<<blocksT_rec, threads>>>(d_res_pr, nt, nrec, 0.0);
    intialArrayGPU<<<blocksT_rec, threads>>>(d_res_vx, nt, nrec, 0.0);
    intialArrayGPU<<<blocksT_rec, threads>>>(d_res_vz, nt, nrec, 0.0);
    intialArrayGPU<<<blocksT_das, threads>>>(d_res_et, nt, ndas, 0.0);

    // Initialize the wavefields for modeling
    intialArrayGPU<<<blocks, threads>>>(d_vz, nz, nx, 0.0);
    intialArrayGPU<<<blocks, threads>>>(d_vx, nz, nx, 0.0);
    intialArrayGPU<<<blocks, threads>>>(d_szz, nz, nx, 0.0);
    intialArrayGPU<<<blocks, threads>>>(d_sxx, nz, nx, 0.0);
    intialArrayGPU<<<blocks, threads>>>(d_sxz, nz, nx, 0.0);

    intialArrayGPU<<<blocks, threads>>>(d_mem_dvz_dz, nz, nx, 0.0);
    intialArrayGPU<<<blocks, threads>>>(d_mem_dvz_dx, nz, nx, 0.0);
    intialArrayGPU<<<blocks, threads>>>(d_mem_dvx_dz, nz, nx, 0.0);
    intialArrayGPU<<<blocks, threads>>>(d_mem_dvx_dx, nz, nx, 0.0);
    intialArrayGPU<<<blocks, threads>>>(d_mem_dszz_dz, nz, nx, 0.0);
    intialArrayGPU<<<blocks, threads>>>(d_mem_dsxx_dx, nz, nx, 0.0);
    intialArrayGPU<<<blocks, threads>>>(d_mem_dsxz_dz, nz, nx, 0.0);
    intialArrayGPU<<<blocks, threads>>>(d_mem_dsxz_dx, nz, nx, 0.0);


    if (is_acoustic) {

      // std::cout << "Forward modeling: acoustic" << std::endl;

      for (int it = 0; it <= nt - 2; it++) {

        // Save and record from the beginning, only for gradient calculation
        if (with_grad) {
          boundaries.field_from_bnd(d_szz, d_sxz, d_sxx, d_vz, d_vx, it);
        }

        // Update the stress
        acoustic_forward_pressure<<<blocks, threads>>>(
            d_vz, d_vx, d_szz, d_mem_dvz_dz, d_mem_dvx_dx, model.d_Lambda,
            cpml.d_K_z_half, cpml.d_a_z_half, cpml.d_b_z_half, cpml.d_K_x,
            cpml.d_a_x, cpml.d_b_x, nz, nx, dt, dz, dx, npml, npad);

        // Add explosive source
        add_source<<<1, threads>>>(d_szz, d_sxx,
                                   survey.vec_source.at(iShot)[it], nz,
                                   survey.vec_z_src.at(iShot),
                                   survey.vec_x_src.at(iShot), dt, d_gauss_amp);

        // Update the velocity
        acoustic_forward_velocity<<<blocks, threads>>>(
            d_vz, d_vx, d_szz, d_mem_dszz_dz, d_mem_dsxx_dx, model.d_ave_Byc_a,
            model.d_ave_Byc_b, cpml.d_K_z, cpml.d_a_z, cpml.d_b_z,
            cpml.d_K_x_half, cpml.d_a_x_half, cpml.d_b_x_half, nz, nx, dt, dz,
            dx, npml, npad);

        // Record syn data recored by geophone: pr = sxx + szz, vx, vz
        record_geo<<<(nrec + 31) / 32, 32>>>(
          d_szz, d_sxx, d_vx, d_vz, nz, d_syn_pr, d_syn_vx, d_syn_vz,
          iShot, it + 1, nt, nrec, survey.d_vec_z_rec.at(iShot),
          survey.d_vec_x_rec.at(iShot));
      
        // Record syn data recored by DAS: et
        record_das<<<(ndas + 31) / 32, 32>>>(
          d_vx, d_vz, nz, d_syn_et,
          iShot, it + 1, nt, ndas, survey.d_vec_z_das.at(iShot),
          survey.d_vec_x_das.at(iShot), survey.d_vec_das_wt_x.at(iShot), 
          survey.d_vec_das_wt_z.at(iShot),survey.gl);
      }
    } else {
      // std::cout << "Forward modeling: elastic" << std::endl;

      // Model the synthetic data: time loop (elastic)
      for (int it = 0; it <= nt - 2; it++) {

        // Save and record from the beginning, only for gradient calculation
        if (with_grad) {
          boundaries.field_from_bnd(d_szz, d_sxz, d_sxx, d_vz, d_vx, it);
        }

        // Update stress
        elastic_forward_stress<<<blocks, threads>>>(
            d_vz, d_vx, d_szz, d_sxx, d_sxz, d_mem_dvz_dz, d_mem_dvz_dx,
            d_mem_dvx_dz, d_mem_dvx_dx, model.d_Lambda, model.d_Mu,
            model.d_ave_Mu, cpml.d_K_z, cpml.d_a_z, cpml.d_b_z, cpml.d_K_z_half,
            cpml.d_a_z_half, cpml.d_b_z_half, cpml.d_K_x, cpml.d_a_x,
            cpml.d_b_x, cpml.d_K_x_half, cpml.d_a_x_half, cpml.d_b_x_half, nz,
            nx, dt, dz, dx, npml, npad);

        // Add explosive source
        add_source<<<1, threads>>>(d_szz, d_sxx,
                                   survey.vec_source.at(iShot)[it], nz,
                                   survey.vec_z_src.at(iShot),
                                   survey.vec_x_src.at(iShot), dt, d_gauss_amp);

        // Update velocity
        elastic_forward_velocity<<<blocks, threads>>>(
            d_vz, d_vx, d_szz, d_sxx, d_sxz, d_mem_dszz_dz, d_mem_dsxz_dx,
            d_mem_dsxz_dz, d_mem_dsxx_dx, model.d_ave_Byc_a, model.d_ave_Byc_b,
            cpml.d_K_z, cpml.d_a_z, cpml.d_b_z, cpml.d_K_z_half,
            cpml.d_a_z_half, cpml.d_b_z_half, cpml.d_K_x, cpml.d_a_x,
            cpml.d_b_x, cpml.d_K_x_half, cpml.d_a_x_half, cpml.d_b_x_half, nz,
            nx, dt, dz, dx, npml, npad);

        // Record syn data recored by geophone: pr = sxx + szz, vx, vz
        record_geo<<<(nrec + 31) / 32, 32>>>(
          d_szz, d_sxx, d_vx, d_vz, nz, d_syn_pr, d_syn_vx, d_syn_vz,
          iShot, it + 1, nt, nrec, survey.d_vec_z_rec.at(iShot),
          survey.d_vec_x_rec.at(iShot));
      
        // Record syn data recored by DAS: et
        record_das<<<(ndas + 31) / 32, 32>>>(
          d_vx, d_vz, nz, d_syn_et,
          iShot, it + 1, nt, ndas, survey.d_vec_z_das.at(iShot),
          survey.d_vec_x_das.at(iShot), survey.d_vec_das_wt_x.at(iShot), 
          survey.d_vec_das_wt_z.at(iShot), survey.gl);

      } // end of forward time loop
    }

    // ------------------------ Compute residuals ------------------------ //

    // Windowing the obs and syn data: pr. vx, vz, and et
    // if (para.if_win()) {
    //   cuda_window<<<blocksT_rec, threads>>>(
    //       nt, nrec, dt, survey.d_vec_win_start.at(iShot),
    //       survey.d_vec_win_end.at(iShot), win_ratio, d_obs_pr);
    //   cuda_window<<<blocksT_rec, threads>>>(
    //       nt, nrec, dt, survey.d_vec_win_start.at(iShot),
    //       survey.d_vec_win_end.at(iShot), win_ratio, d_syn_pr);
    //   cuda_window<<<blocksT_rec, threads>>>(
    //       nt, nrec, dt, survey.d_vec_win_start.at(iShot),
    //       survey.d_vec_win_end.at(iShot), win_ratio, d_obs_vx);
    //   cuda_window<<<blocksT_rec, threads>>>(
    //       nt, nrec, dt, survey.d_vec_win_start.at(iShot),
    //       survey.d_vec_win_end.at(iShot), win_ratio, d_syn_vx);
    //   cuda_window<<<blocksT_rec, threads>>>(
    //       nt, nrec, dt, survey.d_vec_win_start.at(iShot),
    //       survey.d_vec_win_end.at(iShot), win_ratio, d_obs_vz);
    //   cuda_window<<<blocksT_rec, threads>>>(
    //       nt, nrec, dt, survey.d_vec_win_start.at(iShot),
    //       survey.d_vec_win_end.at(iShot), win_ratio, d_syn_vz);
    //   cuda_window<<<blocksT_das, threads>>>(
    //       nt, ndas, dt, survey.d_vec_win_start.at(iShot),
    //       survey.d_vec_win_end.at(iShot), win_ratio, d_obs_et);
    //   cuda_window<<<blocksT_das, threads>>>(
    //       nt, ndas, dt, survey.d_vec_win_start.at(iShot),
    //       survey.d_vec_win_end.at(iShot), win_ratio, d_syn_et);

    // } else {
    //   cuda_window<<<blocksT_rec, threads>>>(nt, nrec, dt, win_ratio, d_obs_pr);
    //   cuda_window<<<blocksT_rec, threads>>>(nt, nrec, dt, win_ratio, d_syn_pr);
    //   cuda_window<<<blocksT_rec, threads>>>(nt, nrec, dt, win_ratio, d_obs_vx);
    //   cuda_window<<<blocksT_rec, threads>>>(nt, nrec, dt, win_ratio, d_syn_vx);
    //   cuda_window<<<blocksT_rec, threads>>>(nt, nrec, dt, win_ratio, d_obs_vz);
    //   cuda_window<<<blocksT_rec, threads>>>(nt, nrec, dt, win_ratio, d_syn_vz);
    //   cuda_window<<<blocksT_das, threads>>>(nt, ndas, dt, win_ratio, d_obs_et);
    //   cuda_window<<<blocksT_das, threads>>>(nt, ndas, dt, win_ratio, d_syn_et);
    // }


    // Calculate source update and filter calculated data
    if (para.if_src_update()) {
      amp_ratio = source_update(nt, dt, nrec, d_obs_pr, d_syn_pr,
                                survey.d_vec_source.at(iShot), survey.d_coef);
      printf("	Source update => Processing shot %d, amp_ratio = %f\n", iShot, amp_ratio);
    }
    amp_ratio = 1.0; // amplitude not used, so set to 1.0

    // TODO: change here to implement different objective functions
    //  objective function

    gpuMinus<<<blocksT_rec, threads>>>(d_res_pr, d_obs_pr, d_syn_pr, nt, nrec);
    gpuMinus<<<blocksT_rec, threads>>>(d_res_vx, d_obs_vx, d_syn_vx, nt, nrec);
    gpuMinus<<<blocksT_rec, threads>>>(d_res_vz, d_obs_vz, d_syn_vz, nt, nrec);
    gpuMinus<<<blocksT_das, threads>>>(d_res_et, d_obs_et, d_syn_et, nt, ndas);

    cuda_cal_objective<<<1, 512>>>(d_obj_pr, d_res_pr, nt * nrec);
    cuda_cal_objective<<<1, 512>>>(d_obj_vx, d_res_vx, nt * nrec);
    cuda_cal_objective<<<1, 512>>>(d_obj_vz, d_res_vz, nt * nrec);
    cuda_cal_objective<<<1, 512>>>(d_obj_et, d_res_et, nt * ndas);

    CHECK(cudaMemcpy(h_obj_pr, d_obj_pr, sizeof(float), cudaMemcpyDeviceToHost));
    CHECK(cudaMemcpy(h_obj_vx, d_obj_vx, sizeof(float), cudaMemcpyDeviceToHost));
    CHECK(cudaMemcpy(h_obj_vz, d_obj_vz, sizeof(float), cudaMemcpyDeviceToHost));
    CHECK(cudaMemcpy(h_obj_et, d_obj_et, sizeof(float), cudaMemcpyDeviceToHost));

    // Calculate objective function
    h_obj += h_obj_pr[0] * weight_pr + h_obj_vx[0] * weight_vx +
             h_obj_vz[0] * weight_vz + h_obj_et[0] * weight_et;

    //  update source again (adjoint)
    if (para.if_src_update()) {
      source_update_adj(nt, dt, nrec, d_res_pr, amp_ratio, survey.d_coef);
    }

    // // windowing again (adjoint)
    // if (para.if_win()) {
    //   cuda_window<<<blocksT_rec, threads>>>(
    //       nt, nrec, dt, survey.d_vec_win_start.at(iShot),
    //       survey.d_vec_win_end.at(iShot), win_ratio, d_res_pr);
    //   cuda_window<<<blocksT_rec, threads>>>(
    //       nt, nrec, dt, survey.d_vec_win_start.at(iShot),
    //       survey.d_vec_win_end.at(iShot), win_ratio, d_res_vx);
    //   cuda_window<<<blocksT_rec, threads>>>(
    //       nt, nrec, dt, survey.d_vec_win_start.at(iShot),
    //       survey.d_vec_win_end.at(iShot), win_ratio, d_res_vz);
    //   cuda_window<<<blocksT_das, threads>>>(
    //       nt, ndas, dt, survey.d_vec_win_start.at(iShot),
    //       survey.d_vec_win_end.at(iShot), win_ratio, d_res_et);
    // } else {
    //   cuda_window<<<blocksT_rec, threads>>>(nt, nrec, dt, win_ratio, d_res_pr);
    //   cuda_window<<<blocksT_rec, threads>>>(nt, nrec, dt, win_ratio, d_res_vx);
    //   cuda_window<<<blocksT_rec, threads>>>(nt, nrec, dt, win_ratio, d_res_vz);
    //   cuda_window<<<blocksT_das, threads>>>(nt, ndas, dt, win_ratio, d_res_et);
    // }


    if (para.if_save_scratch()){

      // copy the residual data from device to host (processed)
      CHECK(cudaMemcpyAsync(survey.vec_res_pr.at(iShot), d_res_pr,
          nt * nrec * sizeof(float), cudaMemcpyDeviceToHost,
          streams[iShot]));
      CHECK(cudaMemcpyAsync(survey.vec_res_vx.at(iShot), d_res_vx,
          nt * nrec * sizeof(float), cudaMemcpyDeviceToHost,
          streams[iShot]));
      CHECK(cudaMemcpyAsync(survey.vec_res_vz.at(iShot), d_res_vz,
          nt * nrec * sizeof(float), cudaMemcpyDeviceToHost,
          streams[iShot]));
      CHECK(cudaMemcpyAsync(survey.vec_res_et.at(iShot), d_res_et,
          nt * ndas * sizeof(float), cudaMemcpyDeviceToHost,
          streams[iShot]));

      // copy the synthetic data from device to host (processed)
      CHECK(cudaMemcpyAsync(survey.vec_syn_pr.at(iShot), d_syn_pr,
                            nt * nrec * sizeof(float), cudaMemcpyDeviceToHost,
                            streams[iShot]));
      CHECK(cudaMemcpyAsync(survey.vec_syn_vx.at(iShot), d_syn_vx,
                            nt * nrec * sizeof(float), cudaMemcpyDeviceToHost,
                            streams[iShot]));
      CHECK(cudaMemcpyAsync(survey.vec_syn_vz.at(iShot), d_syn_vz,
                            nt * nrec * sizeof(float), cudaMemcpyDeviceToHost,
                            streams[iShot]));
      CHECK(cudaMemcpyAsync(survey.vec_syn_et.at(iShot), d_syn_et,
                            nt * ndas * sizeof(float), cudaMemcpyDeviceToHost,
                            streams[iShot]));

      // copy the observed data from device to host (processed)
      CHECK(cudaMemcpyAsync(survey.vec_obs_pr.at(iShot), d_obs_pr,
                            nt * nrec * sizeof(float), cudaMemcpyDeviceToHost,
                            streams[iShot]));
      CHECK(cudaMemcpyAsync(survey.vec_obs_vx.at(iShot), d_obs_vx,
                            nt * nrec * sizeof(float), cudaMemcpyDeviceToHost,
                            streams[iShot]));
      CHECK(cudaMemcpyAsync(survey.vec_obs_vz.at(iShot), d_obs_vz,
                            nt * nrec * sizeof(float), cudaMemcpyDeviceToHost,
                            streams[iShot]));
      CHECK(cudaMemcpyAsync(survey.vec_obs_et.at(iShot), d_obs_et,
                            nt * ndas * sizeof(float), cudaMemcpyDeviceToHost,
                            streams[iShot]));
    }

    // copy the source wavelet from device to host
    CHECK(cudaMemcpy(survey.vec_source.at(iShot), survey.d_vec_source.at(iShot),
                     nt * sizeof(float), cudaMemcpyDeviceToHost));

    // ------------------------ Compute residuals ------------------------ //

    // synchronize all streams
    cudaDeviceSynchronize();

    if (with_grad) {

      // --------------------- Backward ----------------------------
      // initialization
      intialArrayGPU<<<blocks, threads>>>(d_vz_adj, nz, nx, 0.0);
      intialArrayGPU<<<blocks, threads>>>(d_vx_adj, nz, nx, 0.0);
      intialArrayGPU<<<blocks, threads>>>(d_szz_adj, nz, nx, 0.0);
      intialArrayGPU<<<blocks, threads>>>(d_sxx_adj, nz, nx, 0.0);
      intialArrayGPU<<<blocks, threads>>>(d_sxz_adj, nz, nx, 0.0);
      intialArrayGPU<<<blocks, threads>>>(d_mem_dvz_dz, nz, nx, 0.0);
      intialArrayGPU<<<blocks, threads>>>(d_mem_dvz_dx, nz, nx, 0.0);
      intialArrayGPU<<<blocks, threads>>>(d_mem_dvx_dz, nz, nx, 0.0);
      intialArrayGPU<<<blocks, threads>>>(d_mem_dvx_dx, nz, nx, 0.0);
      intialArrayGPU<<<blocks, threads>>>(d_mem_dszz_dz, nz, nx, 0.0);
      intialArrayGPU<<<blocks, threads>>>(d_mem_dsxz_dx, nz, nx, 0.0);
      intialArrayGPU<<<blocks, threads>>>(d_mem_dsxz_dz, nz, nx, 0.0);
      intialArrayGPU<<<blocks, threads>>>(d_mem_dsxx_dx, nz, nx, 0.0);
      intialArrayGPU<<<blocks, threads>>>(model.d_StfGrad, nt, 1, 0.0);
      initialArray(model.h_StfGrad, nt, 0.0);

      if (is_acoustic) {
        intialArrayGPU<<<blocks, threads>>>(d_szz_p1, nz, nx, 0.0);
      }

      if (is_acoustic) {

        // std::cout << "Backward modeling: acoustic" << std::endl;

        for (int it = nt - 2; it >= 0; it--) {
          // source time function kernels
          source_grad<<<1, 1>>>(d_szz_adj, d_sxx_adj, nz, model.d_StfGrad, it,
                                dt, survey.vec_z_src.at(iShot),
                                survey.vec_x_src.at(iShot));

          // save p to szz_plus_one
          assignArrayGPU<<<blocks, threads>>>(d_szz, d_szz_p1, nz, nx);

          // value at T-1
          acoustic_backward_velocity<<<blocks, threads>>>(
              d_vz, d_vx, d_szz, model.d_ave_Byc_a, model.d_ave_Byc_b, nz, nx,
              dt, dz, dx, npml, npad);

          // boundary values
          boundaries.field_to_bnd(d_szz, d_sxz, d_sxx, d_vz, d_vx, it, false);

          // subtract source
          sub_source<<<1, threads>>>(d_szz, d_sxx, survey.vec_source.at(iShot)[it],
                               nz, survey.vec_z_src.at(iShot),
                               survey.vec_x_src.at(iShot), dt, d_gauss_amp);

          // subtract source
          sub_source<<<1, threads>>>(d_szz_p1, d_sxx, survey.vec_source.at(iShot)[it],
                               nz, survey.vec_z_src.at(iShot),
                               survey.vec_x_src.at(iShot), dt, d_gauss_amp);

          acoustic_backward_pressure<<<blocks, threads>>>(
              d_vz, d_vx, d_szz, model.d_Lambda, nz, nx, dt, dz, dx, npml,
              npad);

          boundaries.field_to_bnd(d_szz, d_sxz, d_sxx, d_vz, d_vx, it, true);
          // value at T-2

          // adjoint computation
          acoustic_adjoint_velocity<<<blocks, threads>>>(
              d_vz_adj, d_vx_adj, d_szz_adj, d_mem_dvz_dz, d_mem_dvx_dx,
              d_mem_dszz_dz, d_mem_dsxx_dx, model.d_Lambda, model.d_ave_Byc_a,
              model.d_ave_Byc_b, cpml.d_K_z_half, cpml.d_a_z_half,
              cpml.d_b_z_half, cpml.d_K_x_half, cpml.d_a_x_half,
              cpml.d_b_x_half, cpml.d_K_z, cpml.d_a_z, cpml.d_b_z, cpml.d_K_x,
              cpml.d_a_x, cpml.d_b_x, nz, nx, dt, dz, dx, npml, npad);

          // inject geophone residuals
          inject_geo<<<(nrec + 31) / 32, 32>>>(
              d_szz_adj, d_sxx_adj, d_vx_adj, d_vz_adj, nz, d_res_pr, d_res_vx,
              d_res_vz, it, dt, nt, nrec, survey.d_vec_z_rec.at(iShot), 
              survey.d_vec_x_rec.at(iShot), weight_pr, weight_vx, weight_vz);
          
          // inject das residuals
          inject_das<<<(ndas + 31) / 32, 32>>>(d_vx_adj, d_vz_adj, nz, d_res_et, 
              it, dt, nt, ndas, survey.d_vec_z_das.at(iShot), 
              survey.d_vec_x_das.at(iShot), weight_et, 
              survey.d_vec_das_wt_x.at(iShot), 
              survey.d_vec_das_wt_z.at(iShot), survey.gl);

          acoustic_adjoint_pressure<<<blocks, threads>>>(
              d_vz_adj, d_vx_adj, d_szz_adj, d_mem_dvz_dz, d_mem_dvx_dx,
              d_mem_dszz_dz, d_mem_dsxx_dx, model.d_Lambda, model.d_ave_Byc_a,
              model.d_ave_Byc_b, cpml.d_K_z_half, cpml.d_a_z_half,
              cpml.d_b_z_half, cpml.d_K_x_half, cpml.d_a_x_half,
              cpml.d_b_x_half, cpml.d_K_z, cpml.d_a_z, cpml.d_b_z, cpml.d_K_x,
              cpml.d_a_x, cpml.d_b_x, nz, nx, dt, dz, dx, npml, npad);

          // value at T-1

          // imaging condition
          image_vel_time<<<blocks, threads>>>(
              d_szz, d_szz_p1, d_szz_adj, nz, nx, dt, dz, dx, npml, npad,
              model.d_Vp, model.d_Lambda, model.d_VpGrad);
        }
      } else {
        // std::cout << "Backward modeling: elastic" << std::endl;

        for (int it = nt - 2; it >= 0; it--) {
          // source time function kernels
          source_grad<<<1, 1>>>(d_szz_adj, d_sxx_adj, nz, model.d_StfGrad, it,
                                dt, survey.vec_z_src.at(iShot),
                                survey.vec_x_src.at(iShot));

          // update velocity
          elastic_backward_velocity<<<blocks, threads>>>(
              d_vz, d_vx, d_szz, d_sxx, d_sxz, model.d_ave_Byc_a,
              model.d_ave_Byc_b, nz, nx, dt, dz, dx, npml, npad, d_vz_adj,
              d_vx_adj, model.d_DenGrad);

          // inject boundary wavefields for reconstruction
          boundaries.field_to_bnd(d_szz, d_sxz, d_sxx, d_vz, d_vx, it, false);

          // subtract the source
          sub_source<<<1, threads>>>(
              d_szz, d_sxx, survey.vec_source.at(iShot)[it], nz,
              survey.vec_z_src.at(iShot), survey.vec_x_src.at(iShot), dt,
              d_gauss_amp);

          // update stress
          elastic_backward_stress<<<blocks, threads>>>(
              d_vz, d_vx, d_szz, d_sxx, d_sxz, model.d_Lambda, model.d_Mu,
              model.d_ave_Mu, nz, nx, dt, dz, dx, npml, npad, d_szz_adj,
              d_sxx_adj, d_sxz_adj, model.d_LambdaGrad, model.d_MuGrad);

          // inject boundary wavefields for reconstruction
          boundaries.field_to_bnd(d_szz, d_sxz, d_sxx, d_vz, d_vx, it, true);

          // update velocity of the adjoint wavefield
          elastic_adjoint_velocity<<<blocks, threads>>>(
              d_vz_adj, d_vx_adj, d_szz_adj, d_sxx_adj, d_sxz_adj,
              d_mem_dszz_dz, d_mem_dsxz_dx, d_mem_dsxz_dz, d_mem_dsxx_dx,
              d_mem_dvz_dz, d_mem_dvz_dx, d_mem_dvx_dz, d_mem_dvx_dx,
              model.d_Lambda, model.d_Mu, model.d_ave_Mu, model.d_Den,
              model.d_ave_Byc_a, model.d_ave_Byc_b, cpml.d_K_z_half,
              cpml.d_a_z_half, cpml.d_b_z_half, cpml.d_K_x_half,
              cpml.d_a_x_half, cpml.d_b_x_half, cpml.d_K_z, cpml.d_a_z,
              cpml.d_b_z, cpml.d_K_x, cpml.d_a_x, cpml.d_b_x, nz, nx, dt, dz,
              dx, npml, npad);

          // inject geophone residuals
          inject_geo<<<(nrec + 31) / 32, 32>>>(
            d_szz_adj, d_sxx_adj, d_vx_adj, d_vz_adj, nz, d_res_pr, d_res_vx,
            d_res_vz, it, dt, nt, nrec, survey.d_vec_z_rec.at(iShot), 
            survey.d_vec_x_rec.at(iShot), weight_pr, weight_vx, weight_vz);
        
          // inject das residuals
          inject_das<<<(ndas + 31) / 32, 32>>>(d_vx_adj, d_vz_adj, nz, d_res_et, 
              it, dt, nt, ndas, survey.d_vec_z_das.at(iShot), 
              survey.d_vec_x_das.at(iShot), weight_et, 
              survey.d_vec_das_wt_x.at(iShot),  
              survey.d_vec_das_wt_z.at(iShot), survey.gl);
          
          // update velocity of the adjoint wavefield
          elastic_adjoint_stress<<<blocks, threads>>>(
              d_vz_adj, d_vx_adj, d_szz_adj, d_sxx_adj, d_sxz_adj,
              d_mem_dszz_dz, d_mem_dsxz_dx, d_mem_dsxz_dz, d_mem_dsxx_dx,
              d_mem_dvz_dz, d_mem_dvz_dx, d_mem_dvx_dz, d_mem_dvx_dx,
              model.d_Lambda, model.d_Mu, model.d_ave_Mu, model.d_Den,
              model.d_ave_Byc_a, model.d_ave_Byc_b, cpml.d_K_z_half,
              cpml.d_a_z_half, cpml.d_b_z_half, cpml.d_K_x_half,
              cpml.d_a_x_half, cpml.d_b_x_half, cpml.d_K_z, cpml.d_a_z,
              cpml.d_b_z, cpml.d_K_x, cpml.d_a_x, cpml.d_b_x, nz, nx, dt, dz,
              dx, npml, npad);
        

          // Save wavefield for debug
          //if (iShot == 0 && it % 200 == 0) {
          //  CHECK(cudaMemcpy(h_snap, d_vz_adj, nz * nx * sizeof(float), cudaMemcpyDeviceToHost));
          //  fileBinWrite(h_snap, nz * nx, "SnapGPU_" + std::to_string(it) + ".bin");
          //}

        } // the end of backward time loop
      }
      
      // transfer source gradient to cpu
      CHECK(cudaMemcpy(model.h_StfGrad, model.d_StfGrad, nt * sizeof(float),
                       cudaMemcpyDeviceToHost));

      for (int it = 0; it < nt; it++) {
        grad_stf[iShot * nt + it] = model.h_StfGrad[it];
      }

    } // end bracket of if (with_grad)

    // free memory on GPU
    CHECK(cudaFree(d_syn_pr));
    CHECK(cudaFree(d_syn_vx));
    CHECK(cudaFree(d_syn_vz));
    CHECK(cudaFree(d_syn_et));

    // free memory on CPU
    if (with_grad) {
      CHECK(cudaFree(d_obs_pr));
      CHECK(cudaFree(d_obs_vx));
      CHECK(cudaFree(d_obs_vz));
      CHECK(cudaFree(d_obs_et));
      CHECK(cudaFree(d_res_pr));
      CHECK(cudaFree(d_res_vx));
      CHECK(cudaFree(d_res_vz));
      CHECK(cudaFree(d_res_et));
    }

  } // the end of shot loop

  if (with_grad) {
    if (is_acoustic) {
      // transfer gradients to cpu
      CHECK(cudaMemcpy(model.h_VpGrad, model.d_VpGrad, nz * nx * sizeof(float),
                       cudaMemcpyDeviceToHost));
      for (int i = 0; i < nz; i++) {
        for (int j = 0; j < nx; j++) {
          grad_Vp[i * nx + j] = model.h_VpGrad[j * nz + i];
        }
      }
    } else {
      // std::cout << "Transfer gradients to CPU for elastic gradient" << std::endl;

      // transfer gradients to cpu
      CHECK(cudaMemcpy(model.h_LambdaGrad, model.d_LambdaGrad,
                       nz * nx * sizeof(float), cudaMemcpyDeviceToHost));
      CHECK(cudaMemcpy(model.h_MuGrad, model.d_MuGrad, nz * nx * sizeof(float),
                       cudaMemcpyDeviceToHost));
      CHECK(cudaMemcpy(model.h_DenGrad, model.d_DenGrad,
                       nz * nx * sizeof(float), cudaMemcpyDeviceToHost));
      for (int i = 0; i < nz; i++) {
        for (int j = 0; j < nx; j++) {
          grad_Lambda[i * nx + j] = model.h_LambdaGrad[j * nz + i];
          grad_Mu[i * nx + j] = model.h_MuGrad[j * nz + i];
          grad_Den[i * nx + j] = model.h_DenGrad[j * nz + i];
        }
      }
    }

    if (para.if_save_scratch()) {
      for (int iShot = 0; iShot < group_size; iShot++) {
        // write the residual data to disk (processed)
        fileBinWrite(survey.vec_res_pr.at(iShot),
                     nt * survey.vec_nrec.at(iShot),
                     para.scratch_dir_name() + "/res_proc_shot" +
                         std::to_string(shot_ids[iShot]) + "_pr.bin");
        fileBinWrite(survey.vec_res_vx.at(iShot),
                     nt * survey.vec_nrec.at(iShot),
                     para.scratch_dir_name() + "/res_proc_shot" +
                         std::to_string(shot_ids[iShot]) + "_vx.bin");
        fileBinWrite(survey.vec_res_vz.at(iShot),
                     nt * survey.vec_nrec.at(iShot),
                     para.scratch_dir_name() + "/res_proc_shot" +
                         std::to_string(shot_ids[iShot]) + "_vz.bin");
        fileBinWrite(survey.vec_res_et.at(iShot),
                     nt * survey.vec_ndas.at(iShot),
                     para.scratch_dir_name() + "/res_proc_shot" +
                         std::to_string(shot_ids[iShot]) + "_et.bin");
        // write the synthetic data to disk (processed)
        fileBinWrite(survey.vec_syn_pr.at(iShot),
                     nt * survey.vec_nrec.at(iShot),
                     para.scratch_dir_name() + "/syn_proc_shot" +
                         std::to_string(shot_ids[iShot]) + "_pr.bin");
        fileBinWrite(survey.vec_syn_vx.at(iShot),
                     nt * survey.vec_nrec.at(iShot),
                     para.scratch_dir_name() + "/syn_proc_shot" +
                         std::to_string(shot_ids[iShot]) + "_vx.bin");
        fileBinWrite(survey.vec_syn_vz.at(iShot),
                     nt * survey.vec_nrec.at(iShot),
                     para.scratch_dir_name() + "/syn_proc_shot" +
                         std::to_string(shot_ids[iShot]) + "_vz.bin");
        fileBinWrite(survey.vec_syn_et.at(iShot),
                     nt * survey.vec_ndas.at(iShot),
                     para.scratch_dir_name() + "/syn_proc_shot" +
                         std::to_string(shot_ids[iShot]) + "_et.bin");
        // write the observed data to disk (processed)
        fileBinWrite(survey.vec_obs_pr.at(iShot),
                     nt * survey.vec_nrec.at(iShot),
                     para.scratch_dir_name() + "/obs_proc_shot" +
                         std::to_string(shot_ids[iShot]) + "_pr.bin");
        fileBinWrite(survey.vec_obs_vx.at(iShot),
                     nt * survey.vec_nrec.at(iShot),
                     para.scratch_dir_name() + "/obs_proc_shot" +
                         std::to_string(shot_ids[iShot]) + "_vx.bin");
        fileBinWrite(survey.vec_obs_vz.at(iShot),
                     nt * survey.vec_nrec.at(iShot),
                     para.scratch_dir_name() + "/obs_proc_shot" +
                         std::to_string(shot_ids[iShot]) + "_vz.bin");
        fileBinWrite(survey.vec_obs_et.at(iShot),
                     nt * survey.vec_ndas.at(iShot),
                     para.scratch_dir_name() + "/obs_proc_shot" +
                         std::to_string(shot_ids[iShot]) + "_et.bin");

        if (para.if_src_update()) {
          fileBinWrite(survey.vec_source.at(iShot), nt,
                       para.scratch_dir_name() + "/src_updated" +
                           std::to_string(shot_ids[iShot]) + ".bin");
        }
      }
    }
  }

  // output residual
  h_obj = 0.5 * h_obj;
  *misfit = h_obj;

  // free memory
  free(h_obj_pr);
  free(h_obj_vx);
  free(h_obj_vz);
  free(h_obj_et);
  free(fLambda);
  free(fMu);
  free(fDen);
  //free(h_snap);

  // destroy the streams
  for (int iShot = 0; iShot < group_size; iShot++) {
    CHECK(cudaStreamDestroy(streams[iShot]));
  }

  cudaFree(d_vz);
  cudaFree(d_vx);
  cudaFree(d_szz);
  cudaFree(d_sxx);
  cudaFree(d_sxz);
  cudaFree(d_vz_adj);
  cudaFree(d_vx_adj);
  cudaFree(d_szz_adj);
  cudaFree(d_sxx_adj);
  cudaFree(d_sxz_adj);
  cudaFree(d_mem_dvz_dz);
  cudaFree(d_mem_dvz_dx);
  cudaFree(d_mem_dvx_dz);
  cudaFree(d_mem_dvx_dx);
  cudaFree(d_mem_dszz_dz);
  cudaFree(d_mem_dsxx_dx);
  cudaFree(d_mem_dsxz_dz);
  cudaFree(d_mem_dsxz_dx);
  cudaFree(d_obj_pr);
  cudaFree(d_obj_vx);
  cudaFree(d_obj_vz);
  cudaFree(d_obj_et);
  cudaFree(d_gauss_amp);
}
