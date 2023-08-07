#include "Boundary.h"
#include "Parameter.h"
#include "utils.h"

Bnd::Bnd(const Parameter &para, bool const with_grad) {
  with_grad_ = with_grad;
  if (with_grad_) {
    nz_ = para.nz();
    nx_ = para.nx();
    npml_ = para.npml();
    npad_ = para.npad();
    nt_ = para.nt();

    // save extra 2 layers in the pml for derivative at the boundaries
    nzBnd_ = nz_ - 2 * npml_ - npad_ + 4;
    nxBnd_ = nx_ - 2 * npml_ + 4;
    nLayerStore_ = 5;

    // store n layers
    len_Bnd_vec_ = 2 * (nLayerStore_ * nzBnd_ + nLayerStore_ * nxBnd_);

    // allocate the boundary vector in the device
    CHECK(cudaMalloc((void **)&d_Bnd_szz, len_Bnd_vec_ * nt_ * sizeof(float)));
    CHECK(cudaMalloc((void **)&d_Bnd_sxz, len_Bnd_vec_ * nt_ * sizeof(float)));
    CHECK(cudaMalloc((void **)&d_Bnd_sxx, len_Bnd_vec_ * nt_ * sizeof(float)));

    CHECK(cudaMalloc((void **)&d_Bnd_vz, len_Bnd_vec_ * nt_ * sizeof(float)));
    CHECK(cudaMalloc((void **)&d_Bnd_vx, len_Bnd_vec_ * nt_ * sizeof(float)));
  }
}

Bnd::~Bnd() {
  if (with_grad_) {
    CHECK(cudaFree(d_Bnd_szz));
    CHECK(cudaFree(d_Bnd_sxz));
    CHECK(cudaFree(d_Bnd_sxx));
    CHECK(cudaFree(d_Bnd_vz));
    CHECK(cudaFree(d_Bnd_vx));
  }
}

void Bnd::field_from_bnd(float *d_szz, float *d_sxz, float *d_sxx, float *d_vz,
                         float *d_vx, int indT) {
  from_bnd<<<(len_Bnd_vec_ + 31) / 32, 32>>>(d_szz, d_Bnd_szz, nz_, nx_, nzBnd_,
                                             nxBnd_, len_Bnd_vec_, nLayerStore_,
                                             indT, npml_, npad_, nt_);

  from_bnd<<<(len_Bnd_vec_ + 31) / 32, 32>>>(d_sxz, d_Bnd_sxz, nz_, nx_, nzBnd_,
                                             nxBnd_, len_Bnd_vec_, nLayerStore_,
                                             indT, npml_, npad_, nt_);

  from_bnd<<<(len_Bnd_vec_ + 31) / 32, 32>>>(d_sxx, d_Bnd_sxx, nz_, nx_, nzBnd_,
                                             nxBnd_, len_Bnd_vec_, nLayerStore_,
                                             indT, npml_, npad_, nt_);

  from_bnd<<<(len_Bnd_vec_ + 31) / 32, 32>>>(d_vz, d_Bnd_vz, nz_, nx_, nzBnd_,
                                             nxBnd_, len_Bnd_vec_, nLayerStore_,
                                             indT, npml_, npad_, nt_);

  from_bnd<<<(len_Bnd_vec_ + 31) / 32, 32>>>(d_vx, d_Bnd_vx, nz_, nx_, nzBnd_,
                                             nxBnd_, len_Bnd_vec_, nLayerStore_,
                                             indT, npml_, npad_, nt_);
}

void Bnd::field_to_bnd(float *d_szz, float *d_sxz, float *d_sxx, float *d_vz,
                       float *d_vx, int indT, bool if_stress) {
  if (if_stress) {
    to_bnd<<<(len_Bnd_vec_ + 31) / 32, 32>>>(d_szz, d_Bnd_szz, nz_, nx_, nzBnd_,
                                             nxBnd_, len_Bnd_vec_, nLayerStore_,
                                             indT, npml_, npad_, nt_);

    to_bnd<<<(len_Bnd_vec_ + 31) / 32, 32>>>(d_sxz, d_Bnd_sxz, nz_, nx_, nzBnd_,
                                             nxBnd_, len_Bnd_vec_, nLayerStore_,
                                             indT, npml_, npad_, nt_);

    to_bnd<<<(len_Bnd_vec_ + 31) / 32, 32>>>(d_sxx, d_Bnd_sxx, nz_, nx_, nzBnd_,
                                             nxBnd_, len_Bnd_vec_, nLayerStore_,
                                             indT, npml_, npad_, nt_);

  } else {
    to_bnd<<<(len_Bnd_vec_ + 31) / 32, 32>>>(d_vz, d_Bnd_vz, nz_, nx_, nzBnd_,
                                             nxBnd_, len_Bnd_vec_, nLayerStore_,
                                             indT, npml_, npad_, nt_);

    to_bnd<<<(len_Bnd_vec_ + 31) / 32, 32>>>(d_vx, d_Bnd_vx, nz_, nx_, nzBnd_,
                                             nxBnd_, len_Bnd_vec_, nLayerStore_,
                                             indT, npml_, npad_, nt_);
  }
}