#include "Cpml.h"
#include "Model.h"
#include "Parameter.h"
#include "utils.h"

Cpml::Cpml(Parameter &para, Model &model) {

  int nz = model.nz();
  int nx = model.nx();
  int npml = para.npml();
  int npad = para.npad();
  float f0 = para.f0();
  float dt = para.dt();
  float dz = para.dz();
  float dx = para.dx();

  float CpAve = compCpAve(model.h_Vp, nz * nx);

  // for padding
  K_z = (float *)malloc((nz - npad) * sizeof(float));
  a_z = (float *)malloc((nz - npad) * sizeof(float));
  b_z = (float *)malloc((nz - npad) * sizeof(float));
  K_z_half = (float *)malloc((nz - npad) * sizeof(float));
  a_z_half = (float *)malloc((nz - npad) * sizeof(float));
  b_z_half = (float *)malloc((nz - npad) * sizeof(float));

  K_x = (float *)malloc(nx * sizeof(float));
  a_x = (float *)malloc(nx * sizeof(float));
  b_x = (float *)malloc(nx * sizeof(float));
  K_x_half = (float *)malloc(nx * sizeof(float));
  a_x_half = (float *)malloc(nx * sizeof(float));
  b_x_half = (float *)malloc(nx * sizeof(float));

  cpmlInit(K_z, a_z, b_z, K_z_half, a_z_half, b_z_half, nz - npad, npml, dz, f0,
           dt, CpAve);

  cpmlInit(K_x, a_x, b_x, K_x_half, a_x_half, b_x_half, nx, npml, dx, f0, dt,
           CpAve);

  // for padding
  CHECK(cudaMalloc((void **)&d_K_z, (nz - npad) * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_a_z, (nz - npad) * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_b_z, (nz - npad) * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_K_z_half, (nz - npad) * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_a_z_half, (nz - npad) * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_b_z_half, (nz - npad) * sizeof(float)));

  CHECK(cudaMalloc((void **)&d_K_x, nx * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_a_x, nx * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_b_x, nx * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_K_x_half, nx * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_a_x_half, nx * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_b_x_half, nx * sizeof(float)));

  // for padding
  CHECK(cudaMemcpy(d_K_z, K_z, (nz - npad) * sizeof(float),
                   cudaMemcpyHostToDevice));
  CHECK(cudaMemcpy(d_a_z, a_z, (nz - npad) * sizeof(float),
                   cudaMemcpyHostToDevice));
  CHECK(cudaMemcpy(d_b_z, b_z, (nz - npad) * sizeof(float),
                   cudaMemcpyHostToDevice));
  CHECK(cudaMemcpy(d_K_z_half, K_z_half, (nz - npad) * sizeof(float),
                   cudaMemcpyHostToDevice));
  CHECK(cudaMemcpy(d_a_z_half, a_z_half, (nz - npad) * sizeof(float),
                   cudaMemcpyHostToDevice));
  CHECK(cudaMemcpy(d_b_z_half, b_z_half, (nz - npad) * sizeof(float),
                   cudaMemcpyHostToDevice));

  CHECK(cudaMemcpy(d_K_x, K_x, nx * sizeof(float), cudaMemcpyHostToDevice));
  CHECK(cudaMemcpy(d_a_x, a_x, nx * sizeof(float), cudaMemcpyHostToDevice));
  CHECK(cudaMemcpy(d_b_x, b_x, nx * sizeof(float), cudaMemcpyHostToDevice));
  CHECK(cudaMemcpy(d_K_x_half, K_x_half, nx * sizeof(float),
                   cudaMemcpyHostToDevice));
  CHECK(cudaMemcpy(d_a_x_half, a_x_half, nx * sizeof(float),
                   cudaMemcpyHostToDevice));
  CHECK(cudaMemcpy(d_b_x_half, b_x_half, nx * sizeof(float),
                   cudaMemcpyHostToDevice));
}

Cpml::~Cpml() {
  free(K_z);
  free(a_z);
  free(b_z);
  free(K_z_half);
  free(a_z_half);
  free(b_z_half);
  free(K_x);
  free(a_x);
  free(b_x);
  free(K_x_half);
  free(a_x_half);
  free(b_x_half);

  CHECK(cudaFree(d_K_z));
  CHECK(cudaFree(d_a_z));
  CHECK(cudaFree(d_b_z));
  CHECK(cudaFree(d_K_z_half));
  CHECK(cudaFree(d_a_z_half));
  CHECK(cudaFree(d_b_z_half));
  CHECK(cudaFree(d_K_x));
  CHECK(cudaFree(d_a_x));
  CHECK(cudaFree(d_b_x));
  CHECK(cudaFree(d_K_x_half));
  CHECK(cudaFree(d_a_x_half));
  CHECK(cudaFree(d_b_x_half));
}