#include "IsoOperator.h"
#include "omp.h"
#include <cmath>
#include <cstdlib>
#include <iostream>
#include <stdio.h>
#include <string>
#include <torch/extension.h>
#include <vector>

// Elastic forward modeling operator
void ElasticForward(const torch::Tensor &th_Lambda, const torch::Tensor &th_Mu,
                    const torch::Tensor &th_Den, const torch::Tensor &th_stf,
                    int ngpu, const torch::Tensor &th_shot_ids,
                    const string para_fname) {
  // set default value
  const bool is_acoustic = false;
  const bool with_adj = false;

  // check the gpu and shot number
  const int group_size = th_shot_ids.size(0);
  if (ngpu > group_size) {
    printf("The number of GPUs should be smaller than the number of shots!\n");
    exit(1);
  }

  // transform from torch tensor to 1D native array
  auto Lambda = th_Lambda.data_ptr<float>();
  auto Mu = th_Mu.data_ptr<float>();
  auto Den = th_Den.data_ptr<float>();
  auto stf = th_stf.data_ptr<float>();
  auto sepBars = torch::linspace(0, group_size, ngpu + 1,
                                 torch::TensorOptions().dtype(torch::kFloat32));
  // loop over the GPUs
#pragma omp parallel for num_threads(ngpu)
  for (int i = 0; i < ngpu; i++) {
    int startBar = round(sepBars[i].item<int>());
    int endBar = round(sepBars[i + 1].item<int>());
    auto th_sub_shot_ids = th_shot_ids.narrow(0, startBar, endBar - startBar);
    auto shot_ids = th_sub_shot_ids.data_ptr<int>();

    // launch the forward operator
    Propagator(para_fname, i, th_sub_shot_ids.size(0), shot_ids, Lambda, Mu,
               Den, stf, is_acoustic, with_adj);
  }
}

// Elastic adjoint modeling operator
void ElasticAdjoint(const torch::Tensor &th_Lambda, const torch::Tensor &th_Mu,
                    const torch::Tensor &th_Den, const torch::Tensor &th_stf,
                    int ngpu, const torch::Tensor &th_shot_ids,
                    const string para_fname) {

  // set default value
  const bool is_acoustic = false;
  const bool with_adj = true;

  // check the gpu and shot number
  const int group_size = th_shot_ids.size(0);
  if (ngpu > group_size) {
    printf("The number of GPUs should be smaller than the number of shots!\n");
    exit(1);
  }

  // transform from torch tensor to 1D native array
  auto Lambda = th_Lambda.data_ptr<float>();
  auto Mu = th_Mu.data_ptr<float>();
  auto Den = th_Den.data_ptr<float>();
  auto stf = th_stf.data_ptr<float>();
  auto sepBars = torch::linspace(0, group_size, ngpu + 1,
                                 torch::TensorOptions().dtype(torch::kFloat32));
  // loop over the GPUs
#pragma omp parallel for num_threads(ngpu)
  for (int i = 0; i < ngpu; i++) {
    int startBar = round(sepBars[i].item<int>());
    int endBar = round(sepBars[i + 1].item<int>());
    auto th_sub_shot_ids = th_shot_ids.narrow(0, startBar, endBar - startBar);
    auto shot_ids = th_sub_shot_ids.data_ptr<int>();

    // launch the forward operator
    Propagator(para_fname, i, th_sub_shot_ids.size(0), shot_ids, Lambda, Mu,
               Den, stf, is_acoustic, with_adj);
  }
}

// perform the forward modeling, compare with obs data and return the misfit
std::vector<torch::Tensor> ElasticMisfit(const torch::Tensor &th_Lambda,
                                         const torch::Tensor &th_Mu,
                                         const torch::Tensor &th_Den,
                                         const torch::Tensor &th_stf, int ngpu,
                                         const torch::Tensor &th_shot_ids,
                                         const string para_fname) {

  // default parameters
  bool is_acoustic = false;
  bool with_grad = false;

  // parameters
  const int nz = th_Lambda.size(0);
  const int nx = th_Lambda.size(1);
  const int nSrc = th_stf.size(0);
  const int nt = th_stf.size(1);
  const int group_size = th_shot_ids.size(0);

  // check the gpu and shot number
  if (ngpu > group_size) {
    printf("The number of GPUs should be smaller than the number of shots!\n");
    exit(1);
  }

  // transform from torch tensor to 1D native array
  auto Lambda = th_Lambda.data_ptr<float>();
  auto Mu = th_Mu.data_ptr<float>();
  auto Den = th_Den.data_ptr<float>();
  auto stf = th_stf.data_ptr<float>();
  auto sepBars = torch::linspace(0, group_size, ngpu + 1,
                                 torch::TensorOptions().dtype(torch::kFloat32));
  std::vector<float> vec_misfit(ngpu);
  float misfit_sum = 0.0;

#pragma omp parallel for num_threads(ngpu)
  for (int i = 0; i < ngpu; i++) {

    // initialize the gradient
    float misfit = 0.0;

    // get the shot id
    int startBar = round(sepBars[i].item<int>());
    int endBar = round(sepBars[i + 1].item<int>());
    auto th_sub_shot_ids = th_shot_ids.narrow(0, startBar, endBar - startBar);
    auto shot_ids = th_sub_shot_ids.data_ptr<int>();

    // call the cufd function
    Gradient(para_fname, i, th_sub_shot_ids.size(0), shot_ids, Lambda, Mu, Den,
             stf, &misfit, nullptr, nullptr, nullptr, nullptr, nullptr,
             is_acoustic, with_grad);

    // transform from 1D native array to torch tensor
    vec_misfit.at(i) = misfit;
  }

  // sum the gradients and misfit over all GPUs
  for (int i = 0; i < ngpu; i++) {
    misfit_sum += vec_misfit.at(i);
  }

  // return the results
  return {torch::tensor({misfit_sum})};
}

// gradient calculation
std::vector<torch::Tensor> ElasticGradient(const torch::Tensor &th_Lambda, 
                const torch::Tensor &th_Mu,
                const torch::Tensor &th_Den, const torch::Tensor &th_stf,
                int ngpu, const torch::Tensor &th_shot_ids,
                const string para_fname) {

  // default parameters
  bool is_acoustic = false;
  bool with_grad = true;

  // parameters
  const int nz = th_Lambda.size(0);
  const int nx = th_Lambda.size(1);
  const int nSrc = th_stf.size(0);
  const int nt = th_stf.size(1);
  const int group_size = th_shot_ids.size(0);

  // check the gpu and shot number
  if (ngpu > group_size) {
    printf("The number of GPUs should be smaller than the number of shots!\n");
    exit(1);
  }

  // transform from torch tensor to 1D native array
  auto Lambda = th_Lambda.data_ptr<float>();
  auto Mu = th_Mu.data_ptr<float>();
  auto Den = th_Den.data_ptr<float>();
  auto stf = th_stf.data_ptr<float>();
  auto sepBars = torch::linspace(0, group_size, ngpu + 1,
                                 torch::TensorOptions().dtype(torch::kFloat32));
  std::vector<float> vec_misfit(ngpu);
  std::vector<torch::Tensor> vec_grad_Lambda(ngpu);
  std::vector<torch::Tensor> vec_grad_Mu(ngpu);
  std::vector<torch::Tensor> vec_grad_Den(ngpu);
  std::vector<torch::Tensor> vec_grad_stf(ngpu);
  auto th_grad_Lambda_sum = torch::zeros_like(th_Lambda);
  auto th_grad_Mu_sum = torch::zeros_like(th_Mu);
  auto th_grad_Den_sum = torch::zeros_like(th_Den);
  float misfit_sum = 0.0;

#pragma omp parallel for num_threads(ngpu)
  for (int i = 0; i < ngpu; i++) {

    // initialize the gradient
    float misfit = 0.0;
    auto th_grad_Lambda = torch::zeros_like(th_Lambda);
    auto th_grad_Mu = torch::zeros_like(th_Mu);
    auto th_grad_Den = torch::zeros_like(th_Den);
    auto th_grad_stf = torch::zeros_like(th_stf);

    // get the shot id
    int startBar = round(sepBars[i].item<int>());
    int endBar = round(sepBars[i + 1].item<int>());
    auto th_sub_shot_ids = th_shot_ids.narrow(0, startBar, endBar - startBar);
    auto shot_ids = th_sub_shot_ids.data_ptr<int>();

    // call the cufd function
    Gradient(para_fname, i, th_sub_shot_ids.size(0), shot_ids, Lambda, Mu, Den,
             stf, &misfit, th_grad_Lambda.data_ptr<float>(),
             th_grad_Mu.data_ptr<float>(), th_grad_Den.data_ptr<float>(),
             nullptr, th_grad_stf.data_ptr<float>(), is_acoustic, with_grad);

    // transform from 1D native array to torch tensor
    vec_grad_Lambda.at(i) = th_grad_Lambda;
    vec_grad_Mu.at(i) = th_grad_Mu;
    vec_grad_Den.at(i) = th_grad_Den;
    vec_grad_stf.at(i) = th_grad_stf;
    vec_misfit.at(i) = misfit;
  }

  // sum the gradients and misfit over all GPUs
  for (int i = 0; i < ngpu; i++) {
    th_grad_Lambda_sum += vec_grad_Lambda.at(i);
    th_grad_Mu_sum += vec_grad_Mu.at(i);
    th_grad_Den_sum += vec_grad_Den.at(i);
    misfit_sum += vec_misfit.at(i);
  }

  // return the results
  return {torch::tensor({misfit_sum}), th_grad_Lambda_sum, th_grad_Mu_sum,
          th_grad_Den_sum, vec_grad_stf.at(0)};
}

// Acoustic forward modeling operator
void AcousticForward(const torch::Tensor &th_Lambda, const torch::Tensor &th_Mu,
                     const torch::Tensor &th_Den, const torch::Tensor &th_stf,
                     int ngpu, const torch::Tensor &th_shot_ids,
                     const string para_fname) {

  // set default value
  const bool is_acoustic = true;
  const bool with_adj = false;

  // check the gpu and shot number
  const int group_size = th_shot_ids.size(0);
  if (ngpu > group_size) {
    printf("The number of GPUs should be smaller than the number of shots!\n");
    exit(1);
  }

  // transform from torch tensor to 1D native array
  auto Lambda = th_Lambda.data_ptr<float>();
  auto Mu = th_Mu.data_ptr<float>();
  auto Den = th_Den.data_ptr<float>();
  auto stf = th_stf.data_ptr<float>();
  auto sepBars = torch::linspace(0, group_size, ngpu + 1,
                                 torch::TensorOptions().dtype(torch::kFloat32));
  // loop over the GPUs
#pragma omp parallel for num_threads(ngpu)
  for (int i = 0; i < ngpu; i++) {
    int startBar = round(sepBars[i].item<int>());
    int endBar = round(sepBars[i + 1].item<int>());
    auto th_sub_shot_ids = th_shot_ids.narrow(0, startBar, endBar - startBar);
    auto shot_ids = th_sub_shot_ids.data_ptr<int>();

    // launch the forward operator
    Propagator(para_fname, i, th_sub_shot_ids.size(0), shot_ids, Lambda, Mu,
               Den, stf, is_acoustic, with_adj);
  }
}

// Acoustic adjoint modeling operator
void AcousticAdjoint(const torch::Tensor &th_Lambda, const torch::Tensor &th_Mu,
                     const torch::Tensor &th_Den, const torch::Tensor &th_stf,
                     int ngpu, const torch::Tensor &th_shot_ids,
                     const string para_fname) {

  // set default value
  const bool is_acoustic = true;
  const bool with_adj = true;

  // check the gpu and shot number
  const int group_size = th_shot_ids.size(0);
  if (ngpu > group_size) {
    printf("The number of GPUs should be smaller than the number of shots!\n");
    exit(1);
  }

  // transform from torch tensor to 1D native array
  auto Lambda = th_Lambda.data_ptr<float>();
  auto Mu = th_Mu.data_ptr<float>();
  auto Den = th_Den.data_ptr<float>();
  auto stf = th_stf.data_ptr<float>();
  auto sepBars = torch::linspace(0, group_size, ngpu + 1,
                                 torch::TensorOptions().dtype(torch::kFloat32));
  // loop over the GPUs
#pragma omp parallel for num_threads(ngpu)
  for (int i = 0; i < ngpu; i++) {
    int startBar = round(sepBars[i].item<int>());
    int endBar = round(sepBars[i + 1].item<int>());
    auto th_sub_shot_ids = th_shot_ids.narrow(0, startBar, endBar - startBar);
    auto shot_ids = th_sub_shot_ids.data_ptr<int>();

    // launch the forward operator
    Propagator(para_fname, i, th_sub_shot_ids.size(0), shot_ids, Lambda, Mu,
               Den, stf, is_acoustic, with_adj);
  }
}

// perform the forward modeling, compare with obs data and return the misfit
std::vector<torch::Tensor> AcousticMisfit(const torch::Tensor &th_Lambda,
                                          const torch::Tensor &th_Mu,
                                          const torch::Tensor &th_Den,
                                          const torch::Tensor &th_stf, int ngpu,
                                          const torch::Tensor &th_shot_ids,
                                          const string para_fname) {

  // default parameters
  bool is_acoustic = true;
  bool with_grad = false;

  // parameters
  const int nz = th_Lambda.size(0);
  const int nx = th_Lambda.size(1);
  const int nSrc = th_stf.size(0);
  const int nt = th_stf.size(1);
  const int group_size = th_shot_ids.size(0);

  // check the gpu and shot number
  if (ngpu > group_size) {
    printf("The number of GPUs should be smaller than the number of shots!\n");
    exit(1);
  }

  // transform from torch tensor to 1D native array
  auto Lambda = th_Lambda.data_ptr<float>();
  auto Mu = th_Mu.data_ptr<float>();
  auto Den = th_Den.data_ptr<float>();
  auto stf = th_stf.data_ptr<float>();
  auto sepBars = torch::linspace(0, group_size, ngpu + 1,
                                 torch::TensorOptions().dtype(torch::kFloat32));
  std::vector<float> vec_misfit(ngpu);
  float misfit_sum = 0.0;

#pragma omp parallel for num_threads(ngpu)
  for (int i = 0; i < ngpu; i++) {

    // initialize the gradient
    float misfit = 0.0;

    // get the shot id
    int startBar = round(sepBars[i].item<int>());
    int endBar = round(sepBars[i + 1].item<int>());
    auto th_sub_shot_ids = th_shot_ids.narrow(0, startBar, endBar - startBar);
    auto shot_ids = th_sub_shot_ids.data_ptr<int>();

    // call the cufd function
    Gradient(para_fname, i, th_sub_shot_ids.size(0), shot_ids, Lambda, Mu, Den,
             stf, &misfit, nullptr, nullptr, nullptr, nullptr, nullptr,
             is_acoustic, with_grad);

    // transform from 1D native array to torch tensor
    vec_misfit.at(i) = misfit;
  }

  // sum the gradients and misfit over all GPUs
  for (int i = 0; i < ngpu; i++) {
    misfit_sum += vec_misfit.at(i);
  }

  // return the results
  return {torch::tensor({misfit_sum})};
}

// gradient calculation
std::vector<torch::Tensor>
AcousticGradient(const torch::Tensor &th_Lambda, const torch::Tensor &th_Mu,
                 const torch::Tensor &th_Den, const torch::Tensor &th_stf,
                 int ngpu, const torch::Tensor &th_shot_ids,
                 const string para_fname) {

  // default parameters
  bool is_acoustic = true;
  bool with_grad = true;

  // parameters
  const int nz = th_Lambda.size(0);
  const int nx = th_Lambda.size(1);
  const int nSrc = th_stf.size(0);
  const int nt = th_stf.size(1);
  const int group_size = th_shot_ids.size(0);

  // check the gpu and shot number
  if (ngpu > group_size) {
    printf("The number of GPUs should be smaller than the number of shots!\n");
    exit(1);
  }

  // transform from torch tensor to 1D native array
  auto Lambda = th_Lambda.data_ptr<float>();
  auto Mu = th_Mu.data_ptr<float>();
  auto Den = th_Den.data_ptr<float>();
  auto stf = th_stf.data_ptr<float>();
  auto sepBars = torch::linspace(0, group_size, ngpu + 1,
                                 torch::TensorOptions().dtype(torch::kFloat32));
  std::vector<float> vec_misfit(ngpu);
  std::vector<torch::Tensor> vec_grad_Vp(ngpu);
  std::vector<torch::Tensor> vec_grad_stf(ngpu);
  auto th_grad_Vp_sum = torch::zeros_like(th_Lambda);
  float misfit_sum = 0.0;

#pragma omp parallel for num_threads(ngpu)
  for (int i = 0; i < ngpu; i++) {

    // initialize the gradient
    float misfit = 0.0;
    auto th_grad_Vp = torch::zeros_like(th_Lambda);
    auto th_grad_stf = torch::zeros_like(th_stf);

    // get the shot id
    int startBar = round(sepBars[i].item<int>());
    int endBar = round(sepBars[i + 1].item<int>());
    auto th_sub_shot_ids = th_shot_ids.narrow(0, startBar, endBar - startBar);
    auto shot_ids = th_sub_shot_ids.data_ptr<int>();

    // call the cufd function
    Gradient(para_fname, i, th_sub_shot_ids.size(0), shot_ids, Lambda, Mu, Den,
             stf, &misfit, nullptr, nullptr, nullptr,
             th_grad_Vp.data_ptr<float>(), th_grad_stf.data_ptr<float>(),
             is_acoustic, with_grad);

    // transform from 1D native array to torch tensor
    vec_grad_Vp.at(i) = th_grad_Vp;
    vec_grad_stf.at(i) = th_grad_stf;
    vec_misfit.at(i) = misfit;
  }

  // sum the gradients and misfit over all GPUs
  for (int i = 0; i < ngpu; i++) {
    th_grad_Vp_sum += vec_grad_Vp.at(i);
    misfit_sum += vec_misfit.at(i);
  }

  // return the results
  return {torch::tensor({misfit_sum}), th_grad_Vp_sum, vec_grad_stf.at(0)};
}

PYBIND11_MODULE(TORCH_EXTENSION_NAME, m) {
  m.def("ElasticForward", &ElasticForward, "ElasticForward");
  m.def("ElasticAdjoint", &ElasticAdjoint, "ElasticAdjoint");
  m.def("ElasticMisfit", &ElasticMisfit, "ElasticMisfit");
  m.def("ElasticGradient", &ElasticGradient, "ElasticGradient");
  m.def("AcousticForward", &AcousticForward, "AcousticForward");
  m.def("AcousticAdjoint", &AcousticAdjoint, "AcousticAdjoint");
  m.def("AcousticMisfit", &AcousticMisfit, "AcousticMisfit");
  m.def("AcousticGradient", &AcousticGradient, "AcousticGradient");
}