#define d_vx(z, x) d_vx[(x) * (nz) + (z)]
#define d_vz(z, x) d_vz[(x) * (nz) + (z)]
#define d_szz(z, x) d_szz[(x) * (nz) + (z)] // Pressure
#define d_mem_dszz_dz(z, x) d_mem_dszz_dz[(x) * (nz) + (z)]
#define d_mem_dsxx_dx(z, x) d_mem_dsxx_dx[(x) * (nz) + (z)]
#define d_mem_dvz_dz(z, x) d_mem_dvz_dz[(x) * (nz) + (z)]
#define d_mem_dvx_dx(z, x) d_mem_dvx_dx[(x) * (nz) + (z)]
#define d_Lambda(z, x) d_Lambda[(x) * (nz) + (z)]
#define d_ave_Byc_a(z, x) d_ave_Byc_a[(x) * (nz) + (z)]
#define d_ave_Byc_b(z, x) d_ave_Byc_b[(x) * (nz) + (z)]
#define d_mat_dvz_dz(z, x) d_mat_dvz_dz[(x) * (nz) + (z)]
#define d_mat_dvx_dx(z, x) d_mat_dvx_dx[(x) * (nz) + (z)]
#define d_Vp(z, x) d_Vp[(x) * (nz) + (z)]
#define d_VpGrad(z, x) d_VpGrad[(x) * (nz) + (z)]
#define d_szz_plusone(z, x) d_szz_plusone[(x) * (nz) + (z)]
#define d_szz_adj(z, x) d_szz_adj[(x) * (nz) + (z)]

#include "utils.h"

// acoustic_forward_velocity
// acoustic_forward_stress
// acoustic_backward_stress
// acoustic_backward_velocity
// acoustic_forward_stress
// acoustic_forward_velocity

__global__ void
acoustic_forward_velocity(float *d_vz, float *d_vx, float *d_szz,
                          float *d_mem_dszz_dz, float *d_mem_dsxx_dx,
                          float *d_ave_Byc_a, float *d_ave_Byc_b, float *d_K_z,
                          float *d_a_z, float *d_b_z, float *d_K_x_half,
                          float *d_a_x_half, float *d_b_x_half, int nz, int nx,
                          float dt, float dz, float dx, int npml, int npad) {

  // global index
  int gidz = blockIdx.x * blockDim.x + threadIdx.x;
  int gidx = blockIdx.y * blockDim.y + threadIdx.y;

  float dszz_dz = 0.0;
  float dsxx_dx = 0.0;

  float c1 = 9.0 / 8.0;
  float c2 = 1.0 / 24.0;

  if (gidz >= 2 && gidz <= nz - npad - 3 && gidx >= 2 && gidx <= nx - 3) {

    // update vz
    dszz_dz = (c1 * (d_szz(gidz, gidx) - d_szz(gidz - 1, gidx)) -
               c2 * (d_szz(gidz + 1, gidx) - d_szz(gidz - 2, gidx))) /
              dz;

    if (gidz <= npml || (gidz >= nz - npml - npad - 1)) {
      d_mem_dszz_dz(gidz, gidx) =
          d_b_z[gidz] * d_mem_dszz_dz(gidz, gidx) + d_a_z[gidz] * dszz_dz;
    }

    d_vz(gidz, gidx) += (dszz_dz / d_K_z[gidz] + d_mem_dszz_dz(gidz, gidx)) *
                        d_ave_Byc_a(gidz, gidx) * dt;

    // update vx
    dsxx_dx = (c1 * (d_szz(gidz, gidx + 1) - d_szz(gidz, gidx)) -
               c2 * (d_szz(gidz, gidx + 2) - d_szz(gidz, gidx - 1))) /
              dx;

    if (gidx <= npml || gidx >= nx - npml - 1) {
      d_mem_dsxx_dx(gidz, gidx) = d_b_x_half[gidx] * d_mem_dsxx_dx(gidz, gidx) +
                                  d_a_x_half[gidx] * dsxx_dx;
    }

    d_vx(gidz, gidx) +=
        (dsxx_dx / d_K_x_half[gidx] + d_mem_dsxx_dx(gidz, gidx)) *
        d_ave_Byc_b(gidz, gidx) * dt;

  } else {
    return;
  }
}

__global__ void acoustic_forward_pressure(
    float *d_vz, float *d_vx, float *d_szz, float *d_mem_dvz_dz,
    float *d_mem_dvx_dx, float *d_Lambda, float *d_K_z_half, float *d_a_z_half,
    float *d_b_z_half, float *d_K_x, float *d_a_x, float *d_b_x, int nz, int nx,
    float dt, float dz, float dx, int npml, int npad) {

  int gidz = blockIdx.x * blockDim.x + threadIdx.x;
  int gidx = blockIdx.y * blockDim.y + threadIdx.y;

  float dvz_dz = 0.0;
  float dvx_dx = 0.0;

  float c1 = 9.0 / 8.0;
  float c2 = 1.0 / 24.0;

  if (gidz >= 2 && gidz <= nz - npad - 3 && gidx >= 2 && gidx <= nx - 3) {

    dvz_dz = (c1 * (d_vz(gidz + 1, gidx) - d_vz(gidz, gidx)) -
              c2 * (d_vz(gidz + 2, gidx) - d_vz(gidz - 1, gidx))) / dz;

    dvx_dx = (c1 * (d_vx(gidz, gidx) - d_vx(gidz, gidx - 1)) -
              c2 * (d_vx(gidz, gidx + 1) - d_vx(gidz, gidx - 2))) / dx;

    if (gidz <= npml || (gidz >= nz - npml - npad - 1)) {
      d_mem_dvz_dz(gidz, gidx) = d_b_z_half[gidz] * d_mem_dvz_dz(gidz, gidx) +
                                 d_a_z_half[gidz] * dvz_dz;
      dvz_dz = dvz_dz / d_K_z_half[gidz] + d_mem_dvz_dz(gidz, gidx);
    }
    if (gidx <= npml || gidx >= nx - npml - 1) {
      d_mem_dvx_dx(gidz, gidx) =
          d_b_x[gidx] * d_mem_dvx_dx(gidz, gidx) + d_a_x[gidx] * dvx_dx;
      dvx_dx = dvx_dx / d_K_x[gidx] + d_mem_dvx_dx(gidz, gidx);
    }

    d_szz(gidz, gidx) += d_Lambda(gidz, gidx) * (dvz_dz + dvx_dx) * dt;

  } else {
    return;
  }
}

__global__ void acoustic_backward_velocity(float *d_vz, float *d_vx,
                                           float *d_szz, float *d_ave_Byc_a,
                                           float *d_ave_Byc_b, int nz, int nx,
                                           float dt, float dz, float dx,
                                           int npml, int npad) {

  int gidz = blockIdx.x * blockDim.x + threadIdx.x;
  int gidx = blockIdx.y * blockDim.y + threadIdx.y;

  float dszz_dz = 0.0;
  float dsxx_dx = 0.0;

  float c1 = 9.0 / 8.0;
  float c2 = 1.0 / 24.0;

  if (gidz >= npml + 2 && gidz <= nz - npad - 3 - npml && gidx >= npml + 2 &&
      gidx <= nx - 3 - npml) {

    // update vx
    dsxx_dx = (c1 * (d_szz(gidz, gidx + 1) - d_szz(gidz, gidx)) -
               c2 * (d_szz(gidz, gidx + 2) - d_szz(gidz, gidx - 1))) / dx;
    d_vx(gidz, gidx) -= dsxx_dx * d_ave_Byc_b(gidz, gidx) * dt;

    // update vz
    dszz_dz = (c1 * (d_szz(gidz, gidx) - d_szz(gidz - 1, gidx)) -
               c2 * (d_szz(gidz + 1, gidx) - d_szz(gidz - 2, gidx))) / dz;
    d_vz(gidz, gidx) -= dszz_dz * d_ave_Byc_a(gidz, gidx) * dt;

  } else {
    return;
  }
}

__global__ void acoustic_backward_pressure(float *d_vz, float *d_vx,
                                           float *d_szz, float *d_Lambda,
                                           int nz, int nx, float dt, float dz,
                                           float dx, int npml, int npad) {

  int gidz = blockIdx.x * blockDim.x + threadIdx.x;
  int gidx = blockIdx.y * blockDim.y + threadIdx.y;

  float dvz_dz = 0.0;
  float dvx_dx = 0.0;

  float c1 = 9.0 / 8.0;
  float c2 = 1.0 / 24.0;

  // extension for derivative at the boundaries
  if (gidz >= npml + 2 && gidz <= nz - npad - 3 - npml && gidx >= npml + 2 &&
      gidx <= nx - 3 - npml) {
    // if (gidz>=npml-2 && gidz<=nz-npad+1-npml && gidx>=npml-2 &&
    // gidx<=nx+1-npml) {
    dvz_dz = (c1 * (d_vz(gidz + 1, gidx) - d_vz(gidz, gidx)) -
              c2 * (d_vz(gidz + 2, gidx) - d_vz(gidz - 1, gidx))) / dz;
    dvx_dx = (c1 * (d_vx(gidz, gidx) - d_vx(gidz, gidx - 1)) -
              c2 * (d_vx(gidz, gidx + 1) - d_vx(gidz, gidx - 2))) / dx;
    // d_mat_dvz_dz(gidz, gidx) = dvz_dz;
    // d_mat_dvx_dx(gidz, gidx) = dvx_dx;

    d_szz(gidz, gidx) -= d_Lambda(gidz, gidx) * (dvz_dz + dvx_dx) * dt;
  } else {
    return;
  }
}

__global__ void acoustic_adjoint_velocity(
    float *d_vz, float *d_vx, float *d_szz, float *d_mem_dvz_dz,
    float *d_mem_dvx_dx, float *d_mem_dszz_dz, float *d_mem_dsxx_dx,
    float *d_Lambda, float *d_ave_Byc_a, float *d_ave_Byc_b, float *d_K_z_half,
    float *d_a_z_half, float *d_b_z_half, float *d_K_x_half, float *d_a_x_half,
    float *d_b_x_half, float *d_K_z, float *d_a_z, float *d_b_z, float *d_K_x,
    float *d_a_x, float *d_b_x, int nz, int nx, float dt, float dz, float dx,
    int npml, int npad) {

  int gidz = blockIdx.x * blockDim.x + threadIdx.x;
  int gidx = blockIdx.y * blockDim.y + threadIdx.y;

  float dszz_dz = 0.0;
  float dsxx_dx = 0.0;
  float dpsiz_dz = 0.0;
  float dpsix_dx = 0.0;

  float c1 = 9.0 / 8.0;
  float c2 = 1.0 / 24.0;

  if (gidz >= 2 && gidz <= nz - npad - 3 && gidx >= 2 && gidx <= nx - 3) {

    dsxx_dx = (-c1 * (d_szz(gidz, gidx + 1) - d_szz(gidz, gidx)) +
               c2 * (d_szz(gidz, gidx + 2) - d_szz(gidz, gidx - 1))) / dx;
    dpsix_dx =
        (-c1 * (d_mem_dvx_dx(gidz, gidx + 1) - d_mem_dvx_dx(gidz, gidx)) +
         c2 * (d_mem_dvx_dx(gidz, gidx + 2) - d_mem_dvx_dx(gidz, gidx - 1))) /
        dx;
    
    d_vx(gidz, gidx) += (d_a_x[gidx] * dpsix_dx +
                         d_Lambda(gidz, gidx) * dsxx_dx / d_K_x[gidx] * dt);

    dszz_dz = (-c1 * (d_szz(gidz, gidx) - d_szz(gidz - 1, gidx)) +
               c2 * (d_szz(gidz + 1, gidx) - d_szz(gidz - 2, gidx))) /
              dz;
    dpsiz_dz =
        (-c1 * (d_mem_dvz_dz(gidz, gidx) - d_mem_dvz_dz(gidz - 1, gidx)) +
         c2 * (d_mem_dvz_dz(gidz + 1, gidx) - d_mem_dvz_dz(gidz - 2, gidx))) /
        dz;
    d_vz(gidz, gidx) +=
        (d_a_z_half[gidz] * dpsiz_dz +
         d_Lambda(gidz, gidx) * dszz_dz / d_K_z_half[gidz] * dt);

    // update psiz and psix
    if (gidx <= npml || gidx >= nx - npml - 1) {
      d_mem_dsxx_dx(gidz, gidx) =
          d_b_x_half[gidx] * d_mem_dsxx_dx(gidz, gidx) +
          d_ave_Byc_b(gidz, gidx) * d_vx(gidz, gidx) * dt;
    }
    if (gidz <= npml || (gidz >= nz - npml - npad - 1)) {
      d_mem_dszz_dz(gidz, gidx) =
          d_b_z[gidz] * d_mem_dszz_dz(gidz, gidx) +
          d_ave_Byc_a(gidz, gidx) * d_vz(gidz, gidx) * dt;
    }

  } else {
    return;
  }
}

__global__ void acoustic_adjoint_pressure(
    float *d_vz, float *d_vx, float *d_szz, float *d_mem_dvz_dz,
    float *d_mem_dvx_dx, float *d_mem_dszz_dz, float *d_mem_dsxx_dx,
    float *d_Lambda, float *d_ave_Byc_a, float *d_ave_Byc_b, float *d_K_z_half,
    float *d_a_z_half, float *d_b_z_half, float *d_K_x_half, float *d_a_x_half,
    float *d_b_x_half, float *d_K_z, float *d_a_z, float *d_b_z, float *d_K_x,
    float *d_a_x, float *d_b_x, int nz, int nx, float dt, float dz, float dx,
    int npml, int npad) {

  int gidz = blockIdx.x * blockDim.x + threadIdx.x;
  int gidx = blockIdx.y * blockDim.y + threadIdx.y;

  float dvz_dz = 0.0;
  float dvx_dx = 0.0;
  float dphiz_dz = 0.0;
  float dphix_dx = 0.0;

  float c1 = 9.0 / 8.0;
  float c2 = 1.0 / 24.0;

  if (gidz >= 2 && gidz <= nz - npad - 3 && gidx >= 2 && gidx <= nx - 3) {

    dvz_dz = (-c1 * (d_vz(gidz + 1, gidx) - d_vz(gidz, gidx)) +
              c2 * (d_vz(gidz + 2, gidx) - d_vz(gidz - 1, gidx))) /
             dz;
    dphiz_dz =
        (-c1 * (d_mem_dszz_dz(gidz + 1, gidx) - d_mem_dszz_dz(gidz, gidx)) +
         c2 * (d_mem_dszz_dz(gidz + 2, gidx) - d_mem_dszz_dz(gidz - 1, gidx))) /
        dz;

    // backward difference

    dvx_dx = (-c1 * (d_vx(gidz, gidx) - d_vx(gidz, gidx - 1)) +
              c2 * (d_vx(gidz, gidx + 1) - d_vx(gidz, gidx - 2))) /
             dx;
    dphix_dx =
        (-c1 * (d_mem_dsxx_dx(gidz, gidx) - d_mem_dsxx_dx(gidz, gidx - 1)) +
         c2 * (d_mem_dsxx_dx(gidz, gidx + 1) - d_mem_dsxx_dx(gidz, gidx - 2))) /
        dx;

    // update stress
    d_szz(gidz, gidx) +=
        d_a_x_half[gidx] * dphix_dx + d_a_z[gidz] * dphiz_dz +
        d_ave_Byc_b(gidz, gidx) * dvx_dx / d_K_x_half[gidx] * dt +
        d_ave_Byc_a(gidz, gidx) * dvz_dz / d_K_z[gidz] * dt;

    if (gidx <= npml || gidx >= nx - npml - 1) {
      d_mem_dvx_dx(gidz, gidx) = d_b_x[gidx] * d_mem_dvx_dx(gidz, gidx) +
                                 d_Lambda(gidz, gidx) * d_szz(gidz, gidx) * dt;
    }
    if (gidz <= npml || (gidz >= nz - npml - npad - 1)) {
      d_mem_dvz_dz(gidz, gidx) = d_b_z_half[gidz] * d_mem_dvz_dz(gidz, gidx) +
                                 d_Lambda(gidz, gidx) * d_szz(gidz, gidx) * dt;
    }

  } else {
    return;
  }
}

__global__ void image_vel_time(float *d_szz, float *d_szz_plusone,
                               float *d_szz_adj, int nz, int nx, float dt,
                               float dz, float dx, int npml, int npad,
                               float *d_Vp, float *d_Lambda, float *d_VpGrad) {

  int gidz = blockIdx.x * blockDim.x + threadIdx.x;
  int gidx = blockIdx.y * blockDim.y + threadIdx.y;

  // if (gidz>=2 && gidz<=nz-npad-3 && gidx>=2 && gidx<=nx-3) {
  if (gidz >= npml && gidz <= nz - npml - npad - 1 && gidx >= npml &&
      gidx <= nx - npml - 1) {

    d_szz_plusone(gidz, gidx) = (d_szz_plusone(gidz, gidx) - d_szz(gidz, gidx));
    d_VpGrad(gidz, gidx) += -2.0 / d_Vp(gidz, gidx) *
                            d_szz_plusone(gidz, gidx) * d_szz_adj(gidz, gidx);
  } else {
    return;
  }
}