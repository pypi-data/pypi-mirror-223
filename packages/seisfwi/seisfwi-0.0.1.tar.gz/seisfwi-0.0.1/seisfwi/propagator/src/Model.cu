#include "Model.h"
#include "Parameter.h"
#include "utils.h"
#include <iostream>
#include <string>

// model default constructor
Model::Model() {
  std::cout << "ERROR: You need to supply parameters to initialize models!"
            << std::endl;
  exit(1);
}

// model constructor from parameter file
Model::Model(const Parameter &para, const float *Lambda_, const float *Mu_,
             const float *Den_) {

  nz_ = para.nz();
  nx_ = para.nx();

  dim3 threads(32, 16);
  dim3 blocks((nz_ + 32 - 1) / 32, (nx_ + 16 - 1) / 16);

  h_Lambda = (float *)malloc(nz_ * nx_ * sizeof(float));
  h_Mu = (float *)malloc(nz_ * nx_ * sizeof(float));
  h_Den = (float *)malloc(nz_ * nx_ * sizeof(float));
  h_Vp = (float *)malloc(nz_ * nx_ * sizeof(float));
  h_Vs = (float *)malloc(nz_ * nx_ * sizeof(float));
  h_VpGrad = (float *)malloc(nz_ * nx_ * sizeof(float));
  h_LambdaGrad = (float *)malloc(nz_ * nx_ * sizeof(float));
  h_MuGrad = (float *)malloc(nz_ * nx_ * sizeof(float));
  h_DenGrad = (float *)malloc(nz_ * nx_ * sizeof(float));
  h_StfGrad = (float *)malloc(para.nt() * sizeof(float));


  for (int i = 0; i < nz_ * nx_; i++) {
    if (Lambda_[i] < 0.0) {
      printf("Lambda is negative!");

      // exit program
      exit(1);
    }
    h_Lambda[i] = Lambda_[i];
    h_Mu[i] = Mu_[i];
    h_Den[i] = Den_[i];
  }

  initialArray(h_Vp, nz_ * nx_, 0.0);
  initialArray(h_Vs, nz_ * nx_, 0.0);
  initialArray(h_VpGrad, nz_ * nx_, 0.0);
  initialArray(h_LambdaGrad, nz_ * nx_, 0.0);
  initialArray(h_MuGrad, nz_ * nx_, 0.0);
  initialArray(h_DenGrad, nz_ * nx_, 0.0);
  initialArray(h_StfGrad, para.nt(), 0.0);

  CHECK(cudaMalloc((void **)&d_Lambda, nz_ * nx_ * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_Mu, nz_ * nx_ * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_Den, nz_ * nx_ * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_Vp, nz_ * nx_ * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_Vs, nz_ * nx_ * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_ave_Mu, nz_ * nx_ * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_ave_Byc_a, nz_ * nx_ * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_ave_Byc_b, nz_ * nx_ * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_VpGrad, nz_ * nx_ * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_LambdaGrad, nz_ * nx_ * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_MuGrad, nz_ * nx_ * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_DenGrad, nz_ * nx_ * sizeof(float)));
  CHECK(cudaMalloc((void **)&d_StfGrad, para.nt() * sizeof(float)));
  intialArrayGPU<<<blocks, threads>>>(d_ave_Mu, nz_, nx_, 0.0);
  intialArrayGPU<<<blocks, threads>>>(d_VpGrad, nz_, nx_, 0.0);
  intialArrayGPU<<<blocks, threads>>>(d_LambdaGrad, nz_, nx_, 0.0);
  intialArrayGPU<<<blocks, threads>>>(d_MuGrad, nz_, nx_, 0.0);
  intialArrayGPU<<<blocks, threads>>>(d_DenGrad, nz_, nx_, 0.0);
  intialArrayGPU<<<blocks, threads>>>(d_ave_Byc_a, nz_, nx_, 1.0 / 1000.0);
  intialArrayGPU<<<blocks, threads>>>(d_ave_Byc_b, nz_, nx_, 1.0 / 1000.0);
  intialArrayGPU<<<blocks, threads>>>(d_StfGrad, para.nt(), 1, 0.0);

  CHECK(cudaMemcpy(d_Lambda, h_Lambda, nz_ * nx_ * sizeof(float),
                   cudaMemcpyHostToDevice));
  CHECK(cudaMemcpy(d_Mu, h_Mu, nz_ * nx_ * sizeof(float),
                   cudaMemcpyHostToDevice));
  CHECK(cudaMemcpy(d_Den, h_Den, nz_ * nx_ * sizeof(float),
                   cudaMemcpyHostToDevice));

  velInit<<<blocks, threads>>>(d_Lambda, d_Mu, d_Den, d_Vp, d_Vs, nz_, nx_);
  aveMuInit<<<blocks, threads>>>(d_Mu, d_ave_Mu, nz_, nx_);
  aveBycInit<<<blocks, threads>>>(d_Den, d_ave_Byc_a, d_ave_Byc_b, nz_, nx_);

  CHECK(cudaMemcpy(h_Vp, d_Vp, nz_ * nx_ * sizeof(float),
                   cudaMemcpyDeviceToHost));
  CHECK(cudaMemcpy(h_Vs, d_Vs, nz_ * nx_ * sizeof(float),
                   cudaMemcpyDeviceToHost));

}

Model::~Model() {
  free(h_Vp);
  free(h_Vs);
  free(h_Den);
  free(h_Lambda);
  free(h_Mu);
  free(h_VpGrad);
  CHECK(cudaFree(d_Vp));
  CHECK(cudaFree(d_Vs));
  CHECK(cudaFree(d_Den));
  CHECK(cudaFree(d_Lambda));
  CHECK(cudaFree(d_Mu));
  CHECK(cudaFree(d_ave_Mu));
  CHECK(cudaFree(d_ave_Byc_a));
  CHECK(cudaFree(d_ave_Byc_b));
  CHECK(cudaFree(d_VpGrad));
  CHECK(cudaFree(d_LambdaGrad));
  CHECK(cudaFree(d_MuGrad));
  CHECK(cudaFree(d_DenGrad));
  CHECK(cudaFree(d_StfGrad));
}