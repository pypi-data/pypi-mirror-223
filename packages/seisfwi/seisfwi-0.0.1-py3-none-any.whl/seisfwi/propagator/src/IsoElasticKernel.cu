#define d_vx(z, x) d_vx[(x) * (nz) + (z)]
#define d_vz(z, x) d_vz[(x) * (nz) + (z)]
#define d_sxx(z, x) d_sxx[(x) * (nz) + (z)]
#define d_szz(z, x) d_szz[(x) * (nz) + (z)]
#define d_sxz(z, x) d_sxz[(x) * (nz) + (z)]
#define d_vx_adj(z, x) d_vx_adj[(x) * (nz) + (z)]
#define d_vz_adj(z, x) d_vz_adj[(x) * (nz) + (z)]
#define d_sxx_adj(z, x) d_sxx_adj[(x) * (nz) + (z)]
#define d_szz_adj(z, x) d_szz_adj[(x) * (nz) + (z)]
#define d_sxz_adj(z, x) d_sxz_adj[(x) * (nz) + (z)]
#define d_mem_dszz_dz(z, x) d_mem_dszz_dz[(x) * (nz) + (z)]
#define d_mem_dsxz_dx(z, x) d_mem_dsxz_dx[(x) * (nz) + (z)]
#define d_mem_dsxz_dz(z, x) d_mem_dsxz_dz[(x) * (nz) + (z)]
#define d_mem_dsxx_dx(z, x) d_mem_dsxx_dx[(x) * (nz) + (z)]
#define d_mem_dvz_dz(z, x) d_mem_dvz_dz[(x) * (nz) + (z)]
#define d_mem_dvz_dx(z, x) d_mem_dvz_dx[(x) * (nz) + (z)]
#define d_mem_dvx_dz(z, x) d_mem_dvx_dz[(x) * (nz) + (z)]
#define d_mem_dvx_dx(z, x) d_mem_dvx_dx[(x) * (nz) + (z)]
#define d_Lambda(z, x) d_Lambda[(x) * (nz) + (z)]
#define d_Mu(z, x) d_Mu[(x) * (nz) + (z)]
#define d_Den(z, x) d_Den[(x) * (nz) + (z)]
#define d_ave_Mu(z, x) d_ave_Mu[(x) * (nz) + (z)]
#define d_ave_Byc_a(z, x) d_ave_Byc_a[(x) * (nz) + (z)]
#define d_ave_Byc_b(z, x) d_ave_Byc_b[(x) * (nz) + (z)]
#define d_LambdaGrad(z, x) d_LambdaGrad[(x) * (nz) + (z)]
#define d_MuGrad(z, x) d_MuGrad[(x) * (nz) + (z)]
#define d_DenGrad(z, x) d_DenGrad[(x) * (nz) + (z)]
#include "utils.h"
#include <stdio.h>

// elastic_forward_velocity
// elastic_forward_stress
// elastic_backward_stress
// elastic_backward_velocity
// elastic_forward_stress
// elastic_forward_velocity

// elastic forward modeling: update velocity
__global__ void elastic_forward_velocity(
    float *d_vz, float *d_vx, float *d_szz, float *d_sxx, float *d_sxz,
    float *d_mem_dszz_dz, float *d_mem_dsxz_dx, float *d_mem_dsxz_dz,
    float *d_mem_dsxx_dx, float *d_ave_Byc_a, float *d_ave_Byc_b, float *d_K_z,
    float *d_a_z, float *d_b_z, float *d_K_z_half, float *d_a_z_half,
    float *d_b_z_half, float *d_K_x, float *d_a_x, float *d_b_x,
    float *d_K_x_half, float *d_a_x_half, float *d_b_x_half, int nz, int nx,
    float dt, float dz, float dx, int npml, int npad) {

  // get the global grid index
  int gidz = blockIdx.x * blockDim.x + threadIdx.x;
  int gidx = blockIdx.y * blockDim.y + threadIdx.y;

  // initialize the memory
  float dszz_dz = 0.0;
  float dsxz_dx = 0.0;
  float dsxz_dz = 0.0;
  float dsxx_dx = 0.0;

  // 4th-order FD coefficients
  float c1 = 9.0 / 8.0;
  float c2 = 1.0 / 24.0;

  // update velocity
  if (gidz >= 2 && gidz <= nz - npad - 3 && gidx >= 2 && gidx <= nx - 3) {
    // derivative of stress
    dszz_dz = (c1 * (d_szz(gidz + 1, gidx) - d_szz(gidz, gidx)) -
               c2 * (d_szz(gidz + 2, gidx) - d_szz(gidz - 1, gidx))) / dz;
    dsxz_dx = (c1 * (d_sxz(gidz, gidx) - d_sxz(gidz, gidx - 1)) -
               c2 * (d_sxz(gidz, gidx + 1) - d_sxz(gidz, gidx - 2))) / dx;

    // pml boundary
    if (gidz < npml || (gidz > nz - npml - npad - 1)) {
      d_mem_dszz_dz(gidz, gidx) = d_b_z_half[gidz] * d_mem_dszz_dz(gidz, gidx) +
                                  d_a_z_half[gidz] * dszz_dz;
      dszz_dz = dszz_dz / d_K_z_half[gidz] + d_mem_dszz_dz(gidz, gidx);
    }
    // pml boundary
    if (gidx < npml || gidx > nx - npml) {
      d_mem_dsxz_dx(gidz, gidx) =
          d_b_x[gidx] * d_mem_dsxz_dx(gidz, gidx) + d_a_x[gidx] * dsxz_dx;
      dsxz_dx = dsxz_dx / d_K_x[gidx] + d_mem_dsxz_dx(gidz, gidx);
    }
    // update vz
    d_vz(gidz, gidx) += (dszz_dz + dsxz_dx) * d_ave_Byc_a(gidz, gidx) * dt;

    // derivative of stress
    dsxz_dz = (c1 * (d_sxz(gidz, gidx) - d_sxz(gidz - 1, gidx)) -
               c2 * (d_sxz(gidz + 1, gidx) - d_sxz(gidz - 2, gidx))) / dz;
    dsxx_dx = (c1 * (d_sxx(gidz, gidx + 1) - d_sxx(gidz, gidx)) -
               c2 * (d_sxx(gidz, gidx + 2) - d_sxx(gidz, gidx - 1))) / dx;
    // pml boundary
    if (gidz < npml || (gidz > nz - npml - npad - 1)) {
      d_mem_dsxz_dz(gidz, gidx) = d_b_z[gidz] * d_mem_dsxz_dz(gidz, gidx) + 
                                  d_a_z[gidz] * dsxz_dz;
      dsxz_dz = dsxz_dz / d_K_z[gidz] + d_mem_dsxz_dz(gidz, gidx);
    }
    // pml boundary
    if (gidx < npml || gidx > nx - npml) {
      d_mem_dsxx_dx(gidz, gidx) = d_b_x_half[gidx] * d_mem_dsxx_dx(gidz, gidx) +
                                  d_a_x_half[gidx] * dsxx_dx;
      dsxx_dx = dsxx_dx / d_K_x_half[gidx] + d_mem_dsxx_dx(gidz, gidx);
    }
    // update vx
    d_vx(gidz, gidx) += (dsxz_dz + dsxx_dx) * d_ave_Byc_b(gidz, gidx) * dt;

  } else {
    return;
  }
}

// elastic forward modeling: update stress
__global__ void elastic_forward_stress(
    float *d_vz, float *d_vx, float *d_szz, float *d_sxx, float *d_sxz,
    float *d_mem_dvz_dz, float *d_mem_dvz_dx, float *d_mem_dvx_dz,
    float *d_mem_dvx_dx, float *d_Lambda, float *d_Mu, float *d_ave_Mu,
    float *d_K_z, float *d_a_z, float *d_b_z, float *d_K_z_half,
    float *d_a_z_half, float *d_b_z_half, float *d_K_x, float *d_a_x,
    float *d_b_x, float *d_K_x_half, float *d_a_x_half, float *d_b_x_half,
    int nz, int nx, float dt, float dz, float dx, int npml, int npad) {

  // calculate the global index
  int gidz = blockIdx.x * blockDim.x + threadIdx.x;
  int gidx = blockIdx.y * blockDim.y + threadIdx.y;

  // initialize the derivatives
  float dvz_dz = 0.0;
  float dvx_dx = 0.0;
  float dvx_dz = 0.0;
  float dvz_dx = 0.0;

  // 4th-order FD coefficients
  float c1 = 9.0 / 8.0;
  float c2 = 1.0 / 24.0;

  if (gidz >= 2 && gidz <= nz - npad - 3 && gidx >= 2 && gidx <= nx - 3) {

    // update sxx and szz
    dvz_dz = (c1 * (d_vz(gidz, gidx) - d_vz(gidz - 1, gidx)) -
              c2 * (d_vz(gidz + 1, gidx) - d_vz(gidz - 2, gidx))) / dz;
    dvx_dx = (c1 * (d_vx(gidz, gidx) - d_vx(gidz, gidx - 1)) -
              c2 * (d_vx(gidz, gidx + 1) - d_vx(gidz, gidx - 2))) / dx;

    if (gidz < npml || (gidz > nz - npml - npad - 1)) {
      d_mem_dvz_dz(gidz, gidx) = d_b_z[gidz] * d_mem_dvz_dz(gidz, gidx) + 
                                 d_a_z[gidz] * dvz_dz;
      dvz_dz = dvz_dz / d_K_z[gidz] + d_mem_dvz_dz(gidz, gidx);
    }
    if (gidx < npml || gidx > nx - npml - 1) {
      d_mem_dvx_dx(gidz, gidx) = d_b_x[gidx] * d_mem_dvx_dx(gidz, gidx) + 
                                 d_a_x[gidx] * dvx_dx;
      dvx_dx = dvx_dx / d_K_x[gidx] + d_mem_dvx_dx(gidz, gidx);
    }

    d_szz(gidz, gidx) +=
        ((d_Lambda(gidz, gidx) + 2.0 * d_Mu(gidz, gidx)) * dvz_dz +
          d_Lambda(gidz, gidx) * dvx_dx) * dt;
    d_sxx(gidz, gidx) +=
        (d_Lambda(gidz, gidx) * dvz_dz +
        (d_Lambda(gidz, gidx) + 2.0 * d_Mu(gidz, gidx)) * dvx_dx) * dt;

    // update sxz
    dvx_dz = (c1 * (d_vx(gidz + 1, gidx) - d_vx(gidz, gidx)) -
              c2 * (d_vx(gidz + 2, gidx) - d_vx(gidz - 1, gidx))) / dz;
    dvz_dx = (c1 * (d_vz(gidz, gidx + 1) - d_vz(gidz, gidx)) -
              c2 * (d_vz(gidz, gidx + 2) - d_vz(gidz, gidx - 1))) / dx;

    if (gidz < npml || (gidz > nz - npml - npad - 1)) {
      d_mem_dvx_dz(gidz, gidx) = d_b_z_half[gidz] * d_mem_dvx_dz(gidz, gidx) +
                                 d_a_z_half[gidz] * dvx_dz;
      dvx_dz = dvx_dz / d_K_z_half[gidz] + d_mem_dvx_dz(gidz, gidx);
    }
    if (gidx < npml || gidx > nx - npml - 1) {
      d_mem_dvz_dx(gidz, gidx) = d_b_x_half[gidx] * d_mem_dvz_dx(gidz, gidx) +
                                 d_a_x_half[gidx] * dvz_dx;
      dvz_dx = dvz_dx / d_K_x_half[gidx] + d_mem_dvz_dx(gidz, gidx);
    }

    d_sxz(gidz, gidx) += d_ave_Mu(gidz, gidx) * (dvx_dz + dvz_dx) * dt;

  } else {
    return;
  }
}

// elastic backward modeling: update velocity
__global__ void elastic_backward_velocity(float *d_vz, float *d_vx,
                                          float *d_szz, float *d_sxx,
                                          float *d_sxz, float *d_ave_Byc_a,
                                          float *d_ave_Byc_b, int nz, int nx,
                                          float dt, float dz, float dx,
                                          int npml, int npad, float *d_vz_adj,
                                          float *d_vx_adj, float *d_DenGrad) {

  int gidz = blockIdx.x * blockDim.x + threadIdx.x;
  int gidx = blockIdx.y * blockDim.y + threadIdx.y;

  float dszz_dz = 0.0;
  float dsxz_dx = 0.0;
  float dsxz_dz = 0.0;
  float dsxx_dx = 0.0;

  float c1 = 9.0 / 8.0;
  float c2 = 1.0 / 24.0;

  if (gidz >= npml && gidz <= nz - npad - 1 - npml && gidx >= npml &&
      gidx <= nx - 1 - npml) {
    // update vz
    dszz_dz = (c1 * (d_szz(gidz + 1, gidx) - d_szz(gidz, gidx)) -
               c2 * (d_szz(gidz + 2, gidx) - d_szz(gidz - 1, gidx))) / dz;
    dsxz_dx = (c1 * (d_sxz(gidz, gidx) - d_sxz(gidz, gidx - 1)) -
               c2 * (d_sxz(gidz, gidx + 1) - d_sxz(gidz, gidx - 2))) / dx;

    d_vz(gidz, gidx) -= (dszz_dz + dsxz_dx) * d_ave_Byc_a(gidz, gidx) * dt;

    // update vx
    dsxz_dz = (c1 * (d_sxz(gidz, gidx) - d_sxz(gidz - 1, gidx)) -
               c2 * (d_sxz(gidz + 1, gidx) - d_sxz(gidz - 2, gidx))) / dz;
    dsxx_dx = (c1 * (d_sxx(gidz, gidx + 1) - d_sxx(gidz, gidx)) -
               c2 * (d_sxx(gidz, gidx + 2) - d_sxx(gidz, gidx - 1))) / dx;

    d_vx(gidz, gidx) -= (dsxz_dz + dsxx_dx) * d_ave_Byc_b(gidz, gidx) * dt;

    // cross-correlation image condition: density kernel (spray)
    float grad_ave_Byc_a = -d_vz_adj(gidz, gidx) * (dszz_dz + dsxz_dx) * dt *
                           (-pow(d_ave_Byc_a(gidz, gidx), 2) / 2.0);
    float grad_ave_Byc_b = -d_vx_adj(gidz, gidx) * (dsxz_dz + dsxx_dx) * dt *
                           (-pow(d_ave_Byc_b(gidz, gidx), 2) / 2.0);
    atomicAdd(&d_DenGrad[gidz + nz * gidx], grad_ave_Byc_a);
    atomicAdd(&d_DenGrad[gidz + nz * gidx], grad_ave_Byc_b);
    if (gidz + 1 <= nz - npad - 1 - npml) {
      atomicAdd(&d_DenGrad[gidz + 1 + nz * gidx], grad_ave_Byc_a);
    }
    if (gidx + 1 <= gidx <= nx - 1 - npml) {
      atomicAdd(&d_DenGrad[gidz + nz * (gidx + 1)], grad_ave_Byc_b);
    }
  } else {
    return;
  }
}

// elastic backward modeling: update stress
__global__ void elastic_backward_stress(
    float *d_vz, float *d_vx, float *d_szz, float *d_sxx, float *d_sxz,
    float *d_Lambda, float *d_Mu, float *d_ave_Mu, int nz, int nx, float dt,
    float dz, float dx, int npml, int npad, float *d_szz_adj, float *d_sxx_adj,
    float *d_sxz_adj, float *d_LambdaGrad, float *d_MuGrad) {

  int gidz = blockIdx.x * blockDim.x + threadIdx.x;
  int gidx = blockIdx.y * blockDim.y + threadIdx.y;

  float dvz_dz = 0.0;
  float dvx_dx = 0.0;
  float dvx_dz = 0.0;
  float dvz_dx = 0.0;

  float c1 = 9.0 / 8.0;
  float c2 = 1.0 / 24.0;

  if (gidz >= npml && gidz <= nz - npad - 1 - npml && gidx >= npml &&
      gidx <= nx - 1 - npml) {

    dvz_dz = (c1 * (d_vz(gidz, gidx) - d_vz(gidz - 1, gidx)) -
              c2 * (d_vz(gidz + 1, gidx) - d_vz(gidz - 2, gidx))) / dz;
    dvx_dx = (c1 * (d_vx(gidz, gidx) - d_vx(gidz, gidx - 1)) -
              c2 * (d_vx(gidz, gidx + 1) - d_vx(gidz, gidx - 2))) / dx;

    d_szz(gidz, gidx) -=
        ((d_Lambda(gidz, gidx) + 2.0 * d_Mu(gidz, gidx)) * dvz_dz +
         d_Lambda(gidz, gidx) * dvx_dx) * dt;
    d_sxx(gidz, gidx) -=
        (d_Lambda(gidz, gidx) * dvz_dz +
         (d_Lambda(gidz, gidx) + 2.0 * d_Mu(gidz, gidx)) * dvx_dx) * dt;

    dvx_dz = (c1 * (d_vx(gidz + 1, gidx) - d_vx(gidz, gidx)) -
              c2 * (d_vx(gidz + 2, gidx) - d_vx(gidz - 1, gidx))) / dz;
    dvz_dx = (c1 * (d_vz(gidz, gidx + 1) - d_vz(gidz, gidx)) -
              c2 * (d_vz(gidz, gidx + 2) - d_vz(gidz, gidx - 1))) / dx;

    d_sxz(gidz, gidx) -= d_ave_Mu(gidz, gidx) * (dvx_dz + dvz_dx) * dt;

    // cross-correlation image condition: lambda and mu kernels (spray)
    d_LambdaGrad(gidz, gidx) +=
        -(d_szz_adj(gidz, gidx) + d_sxx_adj(gidz, gidx)) * (dvz_dz + dvx_dx) *
        dt * MEGA;
    d_MuGrad(gidz, gidx) += (-2.0 * d_szz_adj(gidz, gidx) * dvz_dz * dt -
                             2.0 * d_sxx_adj(gidz, gidx) * dvx_dx * dt) * MEGA;

    // spray (atomic add)
    if (d_ave_Mu(gidz, gidx) != 0.0) {
      float scale =
          -d_sxz_adj(gidz, gidx) * (dvx_dz + dvz_dx) * dt *
          d_ave_Mu(gidz, gidx) /
          (1.0 / d_Mu(gidz, gidx) + 1.0 / d_Mu(gidz + 1, gidx) +
           1.0 / d_Mu(gidz, gidx + 1) + 1.0 / d_Mu(gidz + 1, gidx + 1)) * MEGA;
      atomicAdd(&d_MuGrad[gidz + nz * gidx],
                1.0 / pow(d_Mu(gidz, gidx), 2) * scale);
      if (gidz + 1 <= nz - npad - 1 - npml) {
        atomicAdd(&d_MuGrad[gidz + 1 + nz * gidx],
                  1.0 / pow(d_Mu(gidz + 1, gidx), 2) * scale);
      }
      if (gidx + 1 <= gidx <= nx - 1 - npml) {
        atomicAdd(&d_MuGrad[gidz + nz * (gidx + 1)],
                  1.0 / pow(d_Mu(gidz, gidx + 1), 2) * scale);
      }
      if (gidz + 1 <= nz - npad - 1 - npml && gidx + 1 <= nx - 1 - npml) {
        atomicAdd(&d_MuGrad[gidz + 1 + nz * (gidx + 1)],
                  1.0 / pow(d_Mu(gidz + 1, gidx + 1), 2) * scale);
      }
    }
  } else {
    return;
  }
}


// elastic adjoint modeling: update velocity
__global__ void elastic_adjoint_velocity(
  float *d_vz, float *d_vx, float *d_szz, float *d_sxx, float *d_sxz,
  float *d_mem_dszz_dz, float *d_mem_dsxz_dx, float *d_mem_dsxz_dz,
  float *d_mem_dsxx_dx, float *d_mem_dvz_dz, float *d_mem_dvz_dx,
  float *d_mem_dvx_dz, float *d_mem_dvx_dx, float *d_Lambda, float *d_Mu,
  float *d_ave_Mu, float *d_Den, float *d_ave_Byc_a, float *d_ave_Byc_b,
  float *d_K_z_half, float *d_a_z_half, float *d_b_z_half, float *d_K_x_half,
  float *d_a_x_half, float *d_b_x_half, float *d_K_z, float *d_a_z,
  float *d_b_z, float *d_K_x, float *d_a_x, float *d_b_x, int nz, int nx,
  float dt, float dz, float dx, int npml, int npad) {

  int gidz = blockIdx.x * blockDim.x + threadIdx.x;
  int gidx = blockIdx.y * blockDim.y + threadIdx.y;

  float dpsixx_dx = 0.0;
  float dszz_dx = 0.0;
  float dsxx_dx = 0.0;
  float dpsixz_dz = 0.0;
  float dsxz_dz = 0.0;
  float dpsizz_dz = 0.0;
  float dszz_dz = 0.0;
  float dsxx_dz = 0.0;
  float dpsizx_dx = 0.0;
  float dsxz_dx = 0.0;

  float c1 = 9.0 / 8.0;
  float c2 = 1.0 / 24.0;

  // float lambda = d_Lambda(gidz, gidx);
  // float mu = d_Mu(gidz, gidx);

  if (gidz >= 2 && gidz <= nz - npad - 3 && gidx >= 2 && gidx <= nx - 3) {

    // update vx
    dpsixx_dx =
        (-c1 * (d_mem_dvx_dx(gidz, gidx + 1) - d_mem_dvx_dx(gidz, gidx)) +
        c2 * (d_mem_dvx_dx(gidz, gidx + 2) - d_mem_dvx_dx(gidz, gidx - 1))) / dx;

    dszz_dx = (-c1 * (d_szz(gidz, gidx + 1) * d_Lambda(gidz, gidx + 1) - 
                      d_szz(gidz, gidx    ) * d_Lambda(gidz, gidx   )) +
                c2 * (d_szz(gidz, gidx + 2) * d_Lambda(gidz, gidx + 2) - 
                      d_szz(gidz, gidx - 1) * d_Lambda(gidz, gidx - 1))) / dx;

    dsxx_dx = (-c1 * (d_sxx(gidz, gidx + 1) * (d_Lambda(gidz, gidx + 1) + 2.0 * d_Mu(gidz, gidx + 1)) -
                      d_sxx(gidz, gidx    ) * (d_Lambda(gidz, gidx    ) + 2.0 * d_Mu(gidz, gidx    ))) +
                c2 * (d_sxx(gidz, gidx + 2) * (d_Lambda(gidz, gidx + 2) + 2.0 * d_Mu(gidz, gidx + 2)) - 
                      d_sxx(gidz, gidx - 1) * (d_Lambda(gidz, gidx - 1) + 2.0 * d_Mu(gidz, gidx - 1)))) / dx;

    dpsixz_dz =
        (-c1 * (d_mem_dvx_dz(gidz, gidx) - d_mem_dvx_dz(gidz - 1, gidx)) +
        c2 * (d_mem_dvx_dz(gidz + 1, gidx) - d_mem_dvx_dz(gidz - 2, gidx))) / dz;

    dsxz_dz = (-c1 * (d_sxz(gidz    , gidx) * d_ave_Mu(gidz    , gidx) - 
                      d_sxz(gidz - 1, gidx) * d_ave_Mu(gidz - 1, gidx)) +
                c2 * (d_sxz(gidz + 1, gidx) * d_ave_Mu(gidz + 1, gidx) - 
                      d_sxz(gidz - 2, gidx) * d_ave_Mu(gidz - 2, gidx))) / dz;

    d_vx(gidz, gidx) +=
        (d_a_x[gidx] * dpsixx_dx + 
        d_a_z_half[gidz] * dpsixz_dz + 
        dszz_dx / d_K_x[gidx] * dt + 
        dsxx_dx / d_K_x[gidx] * dt +
        dsxz_dz / d_K_z_half[gidz] * dt);


    // update phi_xx_x and phi_xz_z
    if (gidx < npml || gidx > nx - npml - 1) {
      d_mem_dsxx_dx(gidz, gidx) =
          d_b_x_half[gidx] * d_mem_dsxx_dx(gidz, gidx) +
          d_ave_Byc_b(gidz, gidx) * d_vx(gidz, gidx) * dt;
    }
    if (gidz < npml || (gidz > nz - npml - npad - 1)) {
      d_mem_dsxz_dz(gidz, gidx) =
          d_b_z[gidz] * d_mem_dsxz_dz(gidz, gidx) +
          d_ave_Byc_b(gidz, gidx) * d_vx(gidz, gidx) * dt;
    }

    // update vz
    dpsizz_dz =
        (-c1 * (d_mem_dvz_dz(gidz + 1, gidx) - d_mem_dvz_dz(gidz, gidx)) +
        c2 * (d_mem_dvz_dz(gidz + 2, gidx) - d_mem_dvz_dz(gidz - 1, gidx))) / dz;

    dszz_dz = (-c1 * (d_szz(gidz + 1, gidx) * (d_Lambda(gidz + 1, gidx) + 2.0 * d_Mu(gidz + 1, gidx)) - 
                      d_szz(gidz    , gidx) * (d_Lambda(gidz    , gidx) + 2.0 * d_Mu(gidz    , gidx))) +
                c2 * (d_szz(gidz + 2, gidx) * (d_Lambda(gidz + 2, gidx) + 2.0 * d_Mu(gidz + 2, gidx)) - 
                      d_szz(gidz - 1, gidx) * (d_Lambda(gidz - 1, gidx) + 2.0 * d_Mu(gidz - 1, gidx)))) / dz;

    dsxx_dz = (-c1 * (d_sxx(gidz + 1, gidx) * d_Lambda(gidz + 1, gidx) - 
                      d_sxx(gidz    , gidx) * d_Lambda(gidz    , gidx)) +
                c2 * (d_sxx(gidz + 2, gidx) * d_Lambda(gidz + 2, gidx) - 
                      d_sxx(gidz - 1, gidx) * d_Lambda(gidz - 1, gidx))) / dz;

    dpsizx_dx =
        (-c1 * (d_mem_dvz_dx(gidz, gidx) - d_mem_dvz_dx(gidz, gidx - 1)) +
        c2 * (d_mem_dvz_dx(gidz, gidx + 1) - d_mem_dvz_dx(gidz, gidx - 2))) / dx;

    dsxz_dx = (-c1 * (d_sxz(gidz, gidx    ) * d_ave_Mu(gidz, gidx    ) - 
                      d_sxz(gidz, gidx - 1) * d_ave_Mu(gidz, gidx - 1)) +
                c2 * (d_sxz(gidz, gidx + 1) * d_ave_Mu(gidz, gidx + 1) - 
                      d_sxz(gidz, gidx - 2) * d_ave_Mu(gidz, gidx - 2))) / dx;

    d_vz(gidz, gidx) +=
        (d_a_z[gidz] * dpsizz_dz + 
        dszz_dz / d_K_z[gidz] * dt +
        dsxx_dz / d_K_z[gidz] * dt + 
        d_a_x_half[gidx] * dpsizx_dx +
        dsxz_dx / d_K_x_half[gidx] * dt);

    // update phi_xz_x and phi_zz_z
    if (gidx < npml || gidx > nx - npml - 1) {
      d_mem_dsxz_dx(gidz, gidx) =
          d_b_x[gidx] * d_mem_dsxz_dx(gidz, gidx) +
          d_ave_Byc_a(gidz, gidx) * d_vz(gidz, gidx) * dt;
    }
    if (gidz < npml || (gidz > nz - npml - npad - 1)) {
      d_mem_dszz_dz(gidz, gidx) =
          d_b_z_half[gidz] * d_mem_dszz_dz(gidz, gidx) +
          d_ave_Byc_a(gidz, gidx) * d_vz(gidz, gidx) * dt;
    }

  }

  else {
    return;
  }
}


// elastic adjoint modeling: update stress
__global__ void elastic_adjoint_stress(
  float *d_vz, float *d_vx, float *d_szz, float *d_sxx, float *d_sxz,
  float *d_mem_dszz_dz, float *d_mem_dsxz_dx, float *d_mem_dsxz_dz,
  float *d_mem_dsxx_dx, float *d_mem_dvz_dz, float *d_mem_dvz_dx,
  float *d_mem_dvx_dz, float *d_mem_dvx_dx, float *d_Lambda, float *d_Mu,
  float *d_ave_Mu, float *d_Den, float *d_ave_Byc_a, float *d_ave_Byc_b,
  float *d_K_z_half, float *d_a_z_half, float *d_b_z_half, float *d_K_x_half,
  float *d_a_x_half, float *d_b_x_half, float *d_K_z, float *d_a_z,
  float *d_b_z, float *d_K_x, float *d_a_x, float *d_b_x, int nz, int nx,
  float dt, float dz, float dx, int npml, int npad) {

  int gidz = blockIdx.x * blockDim.x + threadIdx.x;
  int gidx = blockIdx.y * blockDim.y + threadIdx.y;

  float dphi_xz_x_dx = 0.0;
  float dvz_dx = 0.0;
  float dphi_xz_z_dz = 0.0;
  float dvx_dz = 0.0;
  float dphi_xx_x_dx = 0.0;
  float dvx_dx = 0.0;
  float dphi_zz_z_dz = 0.0;
  float dvz_dz = 0.0;

  float c1 = 9.0 / 8.0;
  float c2 = 1.0 / 24.0;

  float lambda = d_Lambda(gidz, gidx);
  float mu = d_Mu(gidz, gidx);

  if (gidz >= 2 && gidz <= nz - npad - 3 && gidx >= 2 && gidx <= nx - 3) {

    dphi_xz_x_dx =
        (-c1 * (d_mem_dsxz_dx(gidz, gidx + 1) - d_mem_dsxz_dx(gidz, gidx)) +
          c2 * (d_mem_dsxz_dx(gidz, gidx + 2) - d_mem_dsxz_dx(gidz, gidx - 1))) / dx;

    dvz_dx = (-c1 * (d_vz(gidz, gidx + 1) * d_ave_Byc_a(gidz, gidx + 1) - 
                    d_vz(gidz, gidx    ) * d_ave_Byc_a(gidz, gidx    )) +
              c2 * (d_vz(gidz, gidx + 2) * d_ave_Byc_a(gidz, gidx + 2) - 
                    d_vz(gidz, gidx - 1) * d_ave_Byc_a(gidz, gidx - 1))) / dx;

    dphi_xz_z_dz =
        (-c1 * (d_mem_dsxz_dz(gidz + 1, gidx) - d_mem_dsxz_dz(gidz, gidx)) +
        c2 * (d_mem_dsxz_dz(gidz + 2, gidx) - d_mem_dsxz_dz(gidz - 1, gidx))) / dz;

    dvx_dz = (-c1 * (d_vx(gidz + 1, gidx) * d_ave_Byc_b(gidz + 1, gidx) - 
                    d_vx(gidz    , gidx) * d_ave_Byc_b(gidz    , gidx)) +
              c2 * (d_vx(gidz + 2, gidx) * d_ave_Byc_b(gidz + 2, gidx) - 
                    d_vx(gidz - 1, gidx) * d_ave_Byc_b(gidz - 1, gidx))) / dz;

    // update sxz
    d_sxz(gidz, gidx) += d_a_x[gidx] * dphi_xz_x_dx +
                        dvz_dx / d_K_x[gidx] * dt +
                        d_a_z[gidz] * dphi_xz_z_dz +
                        dvx_dz / d_K_z[gidz] * dt;

    // update psi_zx and psi_xz
    // if(gidx<npml || gidx>nx-npml-1){
    d_mem_dvz_dx(gidz, gidx) = d_b_x_half[gidx] * d_mem_dvz_dx(gidz, gidx) +
                              d_sxz(gidz, gidx) * d_ave_Mu(gidz, gidx) * dt;
    // }
    // if(gidz<npml || gidz>nz-npml-npad-1){
    d_mem_dvx_dz(gidz, gidx) = d_b_z_half[gidz] * d_mem_dvx_dz(gidz, gidx) +
                              d_sxz(gidz, gidx) * d_ave_Mu(gidz, gidx) * dt;
    // }

    dphi_xx_x_dx =
        (-c1 * (d_mem_dsxx_dx(gidz, gidx) - d_mem_dsxx_dx(gidz, gidx - 1)) +
        c2 * (d_mem_dsxx_dx(gidz, gidx + 1) - d_mem_dsxx_dx(gidz, gidx - 2))) / dx;

    dvx_dx = (-c1 * (d_vx(gidz, gidx    ) * d_ave_Byc_b(gidz, gidx    ) - 
                    d_vx(gidz, gidx - 1) * d_ave_Byc_b(gidz, gidx - 1)) +
              c2 * (d_vx(gidz, gidx + 1) * d_ave_Byc_b(gidz, gidx + 1) - 
                    d_vx(gidz, gidx - 2) * d_ave_Byc_b(gidz, gidx - 2))) / dx;

    dphi_zz_z_dz =
        (-c1 * (d_mem_dszz_dz(gidz, gidx) - d_mem_dszz_dz(gidz - 1, gidx)) +
        c2 * (d_mem_dszz_dz(gidz + 1, gidx) - d_mem_dszz_dz(gidz - 2, gidx))) / dz;

    dvz_dz = (-c1 * (d_vz(gidz    , gidx) * d_ave_Byc_a(gidz    , gidx) - 
                    d_vz(gidz - 1, gidx) * d_ave_Byc_a(gidz - 1, gidx)) +
              c2 * (d_vz(gidz + 1, gidx) * d_ave_Byc_a(gidz + 1, gidx) - 
                    d_vz(gidz - 2, gidx) * d_ave_Byc_a(gidz - 2, gidx))) / dz;

    // update sxx and szz
    d_sxx(gidz, gidx) += d_a_x_half[gidx] * dphi_xx_x_dx + dvx_dx / d_K_x_half[gidx] * dt;

    d_szz(gidz, gidx) += d_a_z_half[gidz] * dphi_zz_z_dz + dvz_dz / d_K_z_half[gidz] * dt;

    // update psi_xx and psi_zz
    // if(gidx<npml || gidx>nx-npml-1){
    d_mem_dvx_dx(gidz, gidx) = d_b_x[gidx] * d_mem_dvx_dx(gidz, gidx) +
                              lambda * d_szz(gidz, gidx) * dt +
                              (lambda + 2.0 * mu) * d_sxx(gidz, gidx) * dt;
    // }
    // if(gidz<npml || (gidz>nz-npml-npad-1)){
    d_mem_dvz_dz(gidz, gidx) = d_b_z[gidz] * d_mem_dvz_dz(gidz, gidx) +
                              (lambda + 2.0 * mu) * d_szz(gidz, gidx) * dt +
                              lambda * d_sxx(gidz, gidx) * dt;
    // }

  } else {
    return;
  }
}



// // elastic adjoint modeling: update velocity
// __global__ void elastic_adjoint_velocity(
//     float *d_vz, float *d_vx, float *d_szz, float *d_sxx, float *d_sxz,
//     float *d_mem_dszz_dz, float *d_mem_dsxz_dx, float *d_mem_dsxz_dz,
//     float *d_mem_dsxx_dx, float *d_mem_dvz_dz, float *d_mem_dvz_dx,
//     float *d_mem_dvx_dz, float *d_mem_dvx_dx, float *d_Lambda, float *d_Mu,
//     float *d_ave_Mu, float *d_Den, float *d_ave_Byc_a, float *d_ave_Byc_b,
//     float *d_K_z_half, float *d_a_z_half, float *d_b_z_half, float *d_K_x_half,
//     float *d_a_x_half, float *d_b_x_half, float *d_K_z, float *d_a_z,
//     float *d_b_z, float *d_K_x, float *d_a_x, float *d_b_x, int nz, int nx,
//     float dt, float dz, float dx, int npml, int npad) {

//   int gidz = blockIdx.x * blockDim.x + threadIdx.x;
//   int gidx = blockIdx.y * blockDim.y + threadIdx.y;

//   float dpsixx_dx = 0.0;
//   float dszz_dx = 0.0;
//   float dsxx_dx = 0.0;
//   float dpsixz_dz = 0.0;
//   float dsxz_dz = 0.0;
//   float dpsizz_dz = 0.0;
//   float dszz_dz = 0.0;
//   float dsxx_dz = 0.0;
//   float dpsizx_dx = 0.0;
//   float dsxz_dx = 0.0;

//   float c1 = 9.0 / 8.0;
//   float c2 = 1.0 / 24.0;

//   float lambda = d_Lambda(gidz, gidx);
//   float mu = d_Mu(gidz, gidx);

//   if (gidz >= 2 && gidz <= nz - npad - 3 && gidx >= 2 && gidx <= nx - 3) {

// 		// update vx
// 		dpsixx_dx = (-c1*(d_mem_dvx_dx(gidz,gidx+1)-d_mem_dvx_dx(gidz,gidx)) \
// 			         	+ c2*(d_mem_dvx_dx(gidz,gidx+2)-d_mem_dvx_dx(gidz,gidx-1)))/dx;
// 		dszz_dx = (-c1*(d_szz(gidz,gidx+1)-d_szz(gidz,gidx)) + c2*(d_szz(gidz,gidx+2)-d_szz(gidz,gidx-1)))/dx;
// 		dsxx_dx = (-c1*(d_sxx(gidz,gidx+1)-d_sxx(gidz,gidx)) + c2*(d_sxx(gidz,gidx+2)-d_sxx(gidz,gidx-1)))/dx;
// 		dpsixz_dz = (-c1*(d_mem_dvx_dz(gidz,gidx)-d_mem_dvx_dz(gidz-1,gidx)) \
// 				        + c2*(d_mem_dvx_dz(gidz+1,gidx)-d_mem_dvx_dz(gidz-2,gidx)))/dz;
// 		dsxz_dz = (-c1*(d_sxz(gidz,gidx)-d_sxz(gidz-1,gidx)) + c2*(d_sxz(gidz+1,gidx)-d_sxz(gidz-2,gidx)))/dz;

// 		d_vx(gidz, gidx) += (d_a_x[gidx]*dpsixx_dx + lambda*dszz_dx/d_K_x[gidx]*dt \
// 				+ (lambda+2.0*mu)*dsxx_dx/d_K_x[gidx]*dt + d_a_z_half[gidz]*dpsixz_dz \
// 				+ d_ave_Mu(gidz,gidx)/d_K_z_half[gidz]*dsxz_dz*dt);

// 		//update phi_xx_x and phi_xz_z
// 		if(gidx<npml || gidx>nx-npml-1){
// 			d_mem_dsxx_dx(gidz, gidx) = d_b_x_half[gidx]*d_mem_dsxx_dx(gidz, gidx) + d_ave_Byc_b(gidz, gidx)*d_vx(gidz, gidx)*dt;
// 		}
// 		if(gidz<npml || (gidz>nz-npml-npad-1)){
// 			d_mem_dsxz_dz(gidz, gidx) = d_b_z[gidz]*d_mem_dsxz_dz(gidz, gidx) + d_ave_Byc_b(gidz, gidx)*d_vx(gidz, gidx)*dt;
// 		}

// 	  // update vz
// 		dpsizz_dz = (-c1*(d_mem_dvz_dz(gidz+1,gidx)-d_mem_dvz_dz(gidz,gidx)) \
// 			          + c2*(d_mem_dvz_dz(gidz+2,gidx)-d_mem_dvz_dz(gidz-1,gidx)))/dz;
// 		dszz_dz = (-c1*(d_szz(gidz+1,gidx)-d_szz(gidz,gidx)) + c2*(d_szz(gidz+2,gidx)-d_szz(gidz-1,gidx)))/dz;
// 		dsxx_dz = (-c1*(d_sxx(gidz+1,gidx)-d_sxx(gidz,gidx)) + c2*(d_sxx(gidz+2,gidx)-d_sxx(gidz-1,gidx)))/dz;
// 		dpsizx_dx = (-c1*(d_mem_dvz_dx(gidz,gidx)-d_mem_dvz_dx(gidz,gidx-1)) \
// 			           +c2*(d_mem_dvz_dx(gidz,gidx+1)-d_mem_dvz_dx(gidz,gidx-2)))/dx;
// 		dsxz_dx = (-c1*(d_sxz(gidz,gidx)-d_sxz(gidz,gidx-1)) + c2*(d_sxz(gidz,gidx+1)-d_sxz(gidz,gidx-2)))/dx;

// 		d_vz(gidz, gidx) += (d_a_z[gidz]*dpsizz_dz + (lambda+2.0*mu)*dszz_dz/d_K_z[gidz]*dt \
// 			+ lambda*dsxx_dz/d_K_z[gidz]*dt + d_a_x_half[gidx]*dpsizx_dx \
// 			+ d_ave_Mu(gidz,gidx)/d_K_x_half[gidx]*dsxz_dx*dt);

// 		// update phi_xz_x and phi_zz_z
// 		if(gidx<npml || gidx>nx-npml-1){
// 			d_mem_dsxz_dx(gidz, gidx) = d_b_x[gidx]*d_mem_dsxz_dx(gidz, gidx) + d_ave_Byc_a(gidz, gidx)*d_vz(gidz, gidx)*dt;
// 		}
// 		if(gidz<npml || (gidz>nz-npml-npad-1)){
// 			d_mem_dszz_dz(gidz, gidx) = d_b_z_half[gidz]*d_mem_dszz_dz(gidz, gidx) + d_ave_Byc_a(gidz, gidx)*d_vz(gidz, gidx)*dt;
// 		}

//   }

//   else {
//     return;
//   }
// }

// // elastic adjoint modeling: update stress
// __global__ void elastic_adjoint_stress(
//     float *d_vz, float *d_vx, float *d_szz, float *d_sxx, float *d_sxz,
//     float *d_mem_dszz_dz, float *d_mem_dsxz_dx, float *d_mem_dsxz_dz,
//     float *d_mem_dsxx_dx, float *d_mem_dvz_dz, float *d_mem_dvz_dx,
//     float *d_mem_dvx_dz, float *d_mem_dvx_dx, float *d_Lambda, float *d_Mu,
//     float *d_ave_Mu, float *d_Den, float *d_ave_Byc_a, float *d_ave_Byc_b,
//     float *d_K_z_half, float *d_a_z_half, float *d_b_z_half, float *d_K_x_half,
//     float *d_a_x_half, float *d_b_x_half, float *d_K_z, float *d_a_z,
//     float *d_b_z, float *d_K_x, float *d_a_x, float *d_b_x, int nz, int nx,
//     float dt, float dz, float dx, int npml, int npad) {

//   int gidz = blockIdx.x * blockDim.x + threadIdx.x;
//   int gidx = blockIdx.y * blockDim.y + threadIdx.y;

//   float dphi_xz_x_dx = 0.0;
//   float dvz_dx = 0.0;
//   float dphi_xz_z_dz = 0.0;
//   float dvx_dz = 0.0;
//   float dphi_xx_x_dx = 0.0;
//   float dvx_dx = 0.0;
//   float dphi_zz_z_dz = 0.0;
//   float dvz_dz = 0.0;

//   float c1 = 9.0 / 8.0;
//   float c2 = 1.0 / 24.0;

//   float lambda = d_Lambda(gidz, gidx);
//   float mu = d_Mu(gidz, gidx);

//   if (gidz >= 2 && gidz <= nz - npad - 3 && gidx >= 2 && gidx <= nx - 3) {

//  		dphi_xz_x_dx = (-c1*(d_mem_dsxz_dx(gidz,gidx+1)-d_mem_dsxz_dx(gidz,gidx)) \
// 				            +c2*(d_mem_dsxz_dx(gidz,gidx+2)-d_mem_dsxz_dx(gidz,gidx-1)))/dx;
// 		dvz_dx = (-c1*(d_vz(gidz,gidx+1)-d_vz(gidz,gidx)) + c2*(d_vz(gidz,gidx+2)-d_vz(gidz,gidx-1)))/dx;
// 		dphi_xz_z_dz = (-c1*(d_mem_dsxz_dz(gidz+1,gidx)-d_mem_dsxz_dz(gidz,gidx)) \
// 				            +c2*(d_mem_dsxz_dz(gidz+2,gidx)-d_mem_dsxz_dz(gidz-1,gidx)))/dz;
// 		dvx_dz = (-c1*(d_vx(gidz+1,gidx)-d_vx(gidz,gidx)) + c2*(d_vx(gidz+2,gidx)-d_vx(gidz-1,gidx)))/dz;

// 		// update sxz
// 		d_sxz(gidz,gidx) += d_a_x[gidx]*dphi_xz_x_dx + dvz_dx/d_K_x[gidx]*d_ave_Byc_a(gidz,gidx)*dt \
// 				              + d_a_z[gidz]*dphi_xz_z_dz + dvx_dz/d_K_z[gidz]*d_ave_Byc_b(gidz,gidx)*dt;

// 		// update psi_zx and psi_xz
// 		if(gidx<npml || gidx>nx-npml-1){
// 			d_mem_dvz_dx(gidz,gidx) = d_b_x_half[gidx]*d_mem_dvz_dx(gidz,gidx) + d_sxz(gidz,gidx)*d_ave_Mu(gidz,gidx)*dt;
// 		}
// 		if(gidz<npml || gidz>nz-npml-npad-1){
// 			d_mem_dvx_dz(gidz,gidx) = d_b_z_half[gidz]*d_mem_dvx_dz(gidz,gidx) + d_sxz(gidz,gidx)*d_ave_Mu(gidz,gidx)*dt;
// 		}
		  
// 		dphi_xx_x_dx = (-c1*(d_mem_dsxx_dx(gidz,gidx)-d_mem_dsxx_dx(gidz,gidx-1)) \
// 				            +c2*(d_mem_dsxx_dx(gidz,gidx+1)-d_mem_dsxx_dx(gidz,gidx-2)))/dx;
// 		dvx_dx = (-c1*(d_vx(gidz,gidx)-d_vx(gidz,gidx-1)) + c2*(d_vx(gidz,gidx+1)-d_vx(gidz,gidx-2)))/dx;
// 		dphi_zz_z_dz = (-c1*(d_mem_dszz_dz(gidz,gidx)-d_mem_dszz_dz(gidz-1,gidx)) \
// 				            +c2*(d_mem_dszz_dz(gidz+1,gidx)-d_mem_dszz_dz(gidz-2,gidx)))/dz;
// 		dvz_dz = (-c1*(d_vz(gidz,gidx)-d_vz(gidz-1,gidx)) + c2*(d_vz(gidz+1,gidx)-d_vz(gidz-2,gidx)))/dz;

// 		// update sxx and szz
// 		d_sxx(gidz,gidx) += d_a_x_half[gidx]*dphi_xx_x_dx	+ d_ave_Byc_b(gidz, gidx)*dvx_dx/d_K_x_half[gidx]*dt;;
// 		d_szz(gidz,gidx) += d_a_z_half[gidz]*dphi_zz_z_dz + d_ave_Byc_a(gidz, gidx)*dvz_dz/d_K_z_half[gidz]*dt;

// 		// update psi_xx and psi_zz
// 		if(gidx<npml || gidx>nx-npml-1){
// 			d_mem_dvx_dx(gidz, gidx) = d_b_x[gidx]*d_mem_dvx_dx(gidz, gidx) + lambda*d_szz(gidz, gidx)*dt \
// 				+ (lambda+2.0*mu)*d_sxx(gidz,gidx)*dt;
// 		}
// 		if(gidz<npml || (gidz>nz-npml-npad-1)){
// 			d_mem_dvz_dz(gidz, gidx) = d_b_z[gidz]*d_mem_dvz_dz(gidz, gidx) + (lambda+2.0*mu)*d_szz(gidz, gidx)*dt \
// 				+ lambda*d_sxx(gidz,gidx)*dt;
// 		}

//   } else {
//     return;
//   }
// }




// elastic adjoint modeling: update velocity
// __global__ void elastic_adjoint_velocity(
//     float *d_vz, float *d_vx, float *d_szz, float *d_sxx, float *d_sxz,
//     float *d_mem_dszz_dz, float *d_mem_dsxz_dx, float *d_mem_dsxz_dz,
//     float *d_mem_dsxx_dx, float *d_mem_dvz_dz, float *d_mem_dvz_dx,
//     float *d_mem_dvx_dz, float *d_mem_dvx_dx, float *d_Lambda, float *d_Mu,
//     float *d_ave_Mu, float *d_Den, float *d_ave_Byc_a, float *d_ave_Byc_b,
//     float *d_K_z_half, float *d_a_z_half, float *d_b_z_half, float *d_K_x_half,
//     float *d_a_x_half, float *d_b_x_half, float *d_K_z, float *d_a_z,
//     float *d_b_z, float *d_K_x, float *d_a_x, float *d_b_x, int nz, int nx,
//     float dt, float dz, float dx, int npml, int npad) {

//   int gidz = blockIdx.x * blockDim.x + threadIdx.x;
//   int gidx = blockIdx.y * blockDim.y + threadIdx.y;

//   float dpsixx_dx = 0.0;
//   float dszz_dx = 0.0;
//   float dsxx_dx = 0.0;
//   float dpsixz_dz = 0.0;
//   float dsxz_dz = 0.0;
//   float dpsizz_dz = 0.0;
//   float dszz_dz = 0.0;
//   float dsxx_dz = 0.0;
//   float dpsizx_dx = 0.0;
//   float dsxz_dx = 0.0;

//   float c1 = 9.0 / 8.0;
//   float c2 = 1.0 / 24.0;

//   float lambda = d_Lambda(gidz, gidx);
//   float mu = d_Mu(gidz, gidx);

//   if (gidz >= 2 && gidz <= nz - npad - 3 && gidx >= 2 && gidx <= nx - 3) {

// 		// update vx
// 		dszz_dx = (-c1*(d_szz(gidz,gidx+1)-d_szz(gidz,gidx)) + c2*(d_szz(gidz,gidx+2)-d_szz(gidz,gidx-1)))/dx;
// 		dsxx_dx = (-c1*(d_sxx(gidz,gidx+1)-d_sxx(gidz,gidx)) + c2*(d_sxx(gidz,gidx+2)-d_sxx(gidz,gidx-1)))/dx;
// 		dsxz_dz = (-c1*(d_sxz(gidz,gidx)-d_sxz(gidz-1,gidx)) + c2*(d_sxz(gidz+1,gidx)-d_sxz(gidz-2,gidx)))/dz;

//     // pml boundary
//     // if (gidx < npml || gidx > nx - npml) {
//     //   d_mem_dsxx_dx(gidz, gidx) = d_b_x_half[gidx] * d_mem_dsxx_dx(gidz, gidx) + d_a_x_half[gidx] * dsxx_dx;

//     //   dsxx_dx = dsxx_dx / d_K_x_half[gidx] + d_mem_dsxx_dx(gidz, gidx);
//     //   dszz_dx = dszz_dx / d_K_x_half[gidx] + d_mem_dsxx_dx(gidz, gidx);
//     // }

//     // // pml boundary
//     // if (gidz < npml || (gidz > nz - npml - npad - 1)) {
//     //   d_mem_dsxz_dz(gidz, gidx) = d_b_z[gidz] * d_mem_dsxz_dz(gidz, gidx) + d_a_z[gidz] * dsxz_dz;
//     //   dsxz_dz = dsxz_dz / d_K_z[gidz] + d_mem_dsxz_dz(gidz, gidx);
//     // }

// 		d_vx(gidz, gidx) += ((lambda+2.0*mu)*dsxx_dx + lambda * dszz_dx + d_ave_Mu(gidz,gidx) * dsxz_dz) *dt;
    

// 	  // update vz
// 		dszz_dz = (-c1*(d_szz(gidz+1,gidx)-d_szz(gidz,gidx)) + c2*(d_szz(gidz+2,gidx)-d_szz(gidz-1,gidx)))/dz;
// 		dsxx_dz = (-c1*(d_sxx(gidz+1,gidx)-d_sxx(gidz,gidx)) + c2*(d_sxx(gidz+2,gidx)-d_sxx(gidz-1,gidx)))/dz;
// 		dsxz_dx = (-c1*(d_sxz(gidz,gidx)-d_sxz(gidz,gidx-1)) + c2*(d_sxz(gidz,gidx+1)-d_sxz(gidz,gidx-2)))/dx;

//     // // pml boundary
//     // if (gidz < npml || (gidz > nz - npml - npad - 1)) {
//     //   d_mem_dszz_dz(gidz, gidx) = d_b_z_half[gidz] * d_mem_dszz_dz(gidz, gidx) + d_a_z_half[gidz] * dszz_dz;

//     //   dszz_dz = dszz_dz / d_K_z_half[gidz] + d_mem_dszz_dz(gidz, gidx);
//     //   dsxx_dz = dsxx_dz / d_K_z_half[gidz] + d_mem_dszz_dz(gidz, gidx);
//     // }

//     // // pml boundary
//     // if (gidx < npml || gidx > nx - npml) {
//     //   d_mem_dsxz_dx(gidz, gidx) = d_b_x[gidx] * d_mem_dsxz_dx(gidz, gidx) + d_a_x[gidx] * dsxz_dx;
//     //   dsxz_dx = dsxz_dx / d_K_x[gidx] + d_mem_dsxz_dx(gidz, gidx);
//     // }
  
//     d_vz(gidz, gidx) += ((lambda+2.0*mu)*dszz_dz + lambda * dsxx_dz + d_ave_Mu(gidz,gidx) * dsxz_dx) *dt;

//   }

//   else {
//     return;
//   }
// }

// // elastic adjoint modeling: update stress
// __global__ void elastic_adjoint_stress(
//     float *d_vz, float *d_vx, float *d_szz, float *d_sxx, float *d_sxz,
//     float *d_mem_dszz_dz, float *d_mem_dsxz_dx, float *d_mem_dsxz_dz,
//     float *d_mem_dsxx_dx, float *d_mem_dvz_dz, float *d_mem_dvz_dx,
//     float *d_mem_dvx_dz, float *d_mem_dvx_dx, float *d_Lambda, float *d_Mu,
//     float *d_ave_Mu, float *d_Den, float *d_ave_Byc_a, float *d_ave_Byc_b,
//     float *d_K_z_half, float *d_a_z_half, float *d_b_z_half, float *d_K_x_half,
//     float *d_a_x_half, float *d_b_x_half, float *d_K_z, float *d_a_z,
//     float *d_b_z, float *d_K_x, float *d_a_x, float *d_b_x, int nz, int nx,
//     float dt, float dz, float dx, int npml, int npad) {

//   int gidz = blockIdx.x * blockDim.x + threadIdx.x;
//   int gidx = blockIdx.y * blockDim.y + threadIdx.y;

//   float dphi_xz_x_dx = 0.0;
//   float dvz_dx = 0.0;
//   float dphi_xz_z_dz = 0.0;
//   float dvx_dz = 0.0;
//   float dphi_xx_x_dx = 0.0;
//   float dvx_dx = 0.0;
//   float dphi_zz_z_dz = 0.0;
//   float dvz_dz = 0.0;

//   float c1 = 9.0 / 8.0;
//   float c2 = 1.0 / 24.0;

//   float lambda = d_Lambda(gidz, gidx);
//   float mu = d_Mu(gidz, gidx);

//   if (gidz >= 2 && gidz <= nz - npad - 3 && gidx >= 2 && gidx <= nx - 3) {


//   	// update sxz
// 		dvz_dx = (-c1*(d_vz(gidz,gidx+1)-d_vz(gidz,gidx)) + c2*(d_vz(gidz,gidx+2)-d_vz(gidz,gidx-1)))/dx;
// 		dvx_dz = (-c1*(d_vx(gidz+1,gidx)-d_vx(gidz,gidx)) + c2*(d_vx(gidz+2,gidx)-d_vx(gidz-1,gidx)))/dz;

//     // if (gidz < npml || (gidz > nz - npml - npad - 1)) {
//     //   d_mem_dvx_dz(gidz, gidx) = d_b_z_half[gidz] * d_mem_dvx_dz(gidz, gidx) + d_a_z_half[gidz] * dvx_dz;
//     //   dvx_dz = dvx_dz / d_K_z_half[gidz] + d_mem_dvx_dz(gidz, gidx);
//     // }
//     // if (gidx < npml || gidx > nx - npml - 1) {
//     //   d_mem_dvz_dx(gidz, gidx) = d_b_x_half[gidx] * d_mem_dvz_dx(gidz, gidx) + d_a_x_half[gidx] * dvz_dx;
//     //   dvz_dx = dvz_dx / d_K_x_half[gidx] + d_mem_dvz_dx(gidz, gidx);
//     // }

// 		// update sxz
// 		d_sxz(gidz,gidx) +=  dvz_dx * d_ave_Byc_a(gidz,gidx)*dt + dvx_dz * d_ave_Byc_b(gidz,gidx)*dt;

//     // update sxx and szz
// 		dvx_dx = (-c1*(d_vx(gidz,gidx)-d_vx(gidz,gidx-1)) + c2*(d_vx(gidz,gidx+1)-d_vx(gidz,gidx-2)))/dx;
// 		dvz_dz = (-c1*(d_vz(gidz,gidx)-d_vz(gidz-1,gidx)) + c2*(d_vz(gidz+1,gidx)-d_vz(gidz-2,gidx)))/dz;

//     // if (gidz < npml || (gidz > nz - npml - npad - 1)) {
//     //   d_mem_dvz_dz(gidz, gidx) = d_b_z[gidz] * d_mem_dvz_dz(gidz, gidx) + d_a_z[gidz] * dvz_dz;
//     //   dvz_dz = dvz_dz / d_K_z[gidz] + d_mem_dvz_dz(gidz, gidx);
//     // }
//     // if (gidx < npml || gidx > nx - npml - 1) {
//     //   d_mem_dvx_dx(gidz, gidx) = d_b_x[gidx] * d_mem_dvx_dx(gidz, gidx) + d_a_x[gidx] * dvx_dx;
//     //   dvx_dx = dvx_dx / d_K_x[gidx] + d_mem_dvx_dx(gidz, gidx);
//     // }

// 		// update sxx and szz
// 		d_sxx(gidz,gidx) += d_ave_Byc_b(gidz, gidx) * dvx_dx * dt;
// 		d_szz(gidz,gidx) += d_ave_Byc_a(gidz, gidx) * dvz_dz * dt;

//   } else {
//     return;
//   }
// }