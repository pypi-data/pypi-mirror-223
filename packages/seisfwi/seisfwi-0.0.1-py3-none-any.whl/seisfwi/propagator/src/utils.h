#ifndef utils_H__
#define utils_H__

#include "cufft.h"
#include "rapidjson/document.h"
#include "rapidjson/rapidjson.h"
#include <cmath>
#include <cuComplex.h>
#include <cuda_runtime.h>
#include <iostream>
#include <stdio.h>
#include <string>
#include <vector>

#define PI (3.141592653589793238462643383279502884197169)
#define MEGA 1 // 1e6

#define TX 32
#define TY 16

#define DIVCONST 1e-9

#define CHECK(call)                                                            \
  {                                                                            \
    const cudaError_t error = call;                                            \
    if (error != cudaSuccess) {                                                \
      printf("Error: %s:%d, ", __FILE__, __LINE__);                            \
      printf("code:%d, reason: %s\n", error, cudaGetErrorString(error));       \
      exit(1);                                                                 \
    }                                                                          \
  }

// IO tools
void fileBinLoad(float *h_bin, int size, std::string fname);

void fileBinWrite(float *h_bin, int size, std::string fname);

void fileBinWriteDouble(double *h_bin, int size, std::string fname);

// Array tools
void initialArray(float *ip, int size, float value);

void initialArray(double *ip, int size, double value);

__global__ void intialArrayGPU(float *ip, int nx, int ny, float value);

__global__ void assignArrayGPU(float *ip_in, float *ip_out, int nx, int ny);

void displayArray(std::string s, float *ip, int nx, int ny);

// Model tools
__global__ void moduliInit(float *d_Vp, float *d_Vs, float *d_Den,
                           float *d_Lambda, float *d_Mu, int nx, int ny);

__global__ void velInit(float *d_Lambda, float *d_Mu, float *d_Den, float *d_Vp,
                        float *d_Vs, int nx, int ny);

__global__ void aveMuInit(float *d_Mu, float *d_ave_Mu, int nx, int ny);

__global__ void aveBycInit(float *d_Den, float *d_ave_Byc_a, float *d_ave_Byc_b,
                           int nx, int ny);

float compCpAve(float *array, int N);

void compCourantNumber(float *h_Vp, int size, float dt, float dz, float dx);

void cpmlInit(float *K, float *a, float *b, float *K_half, float *a_half,
              float *b_half, int N, int npml, float dh, float f0, float dt,
              float CpAve);

// GPU math tools
__global__ void gpuMinus(float *d_out, float *d_in1, float *d_in2, int nx,
                         int ny);

// Objective function tools
__global__ void cuda_cal_objective(float *obj, float *err, int ng);

float cal_objective(float *array, int N);

__global__ void cuda_normal_misfit(int nrec, float *d_cross_normfact,
                                   float *d_obs_normfact, float *d_cal_normfact,
                                   float *misfit, float *d_weights,
                                   float src_weight);

__global__ void
cuda_normal_adjoint_source(int nt, int nrec, float *d_obs_normfact,
                           float *d_cal_normfact, float *d_cross_normfact,
                           float *d_obs, float *d_data, float *d_res,
                           float *d_weights, float src_weight);

// Acoustic Kernels
__global__ void
acoustic_forward_velocity(float *d_vz, float *d_vx, float *d_szz,
                          float *d_mem_dszz_dz, float *d_mem_dsxx_dx,
                          float *d_ave_Byc_a, float *d_ave_Byc_b, float *d_K_z,
                          float *d_a_z, float *d_b_z, float *d_K_x_half,
                          float *d_a_x_half, float *d_b_x_half, int nz, int nx,
                          float dt, float dz, float dx, int npml, int npad);

__global__ void acoustic_forward_pressure(
    float *d_vz, float *d_vx, float *d_szz, float *d_mem_dvz_dz,
    float *d_mem_dvx_dx, float *d_Lambda, float *d_K_z_half, float *d_a_z_half,
    float *d_b_z_half, float *d_K_x, float *d_a_x, float *d_b_x, int nz, int nx,
    float dt, float dz, float dx, int npml, int npad);

__global__ void acoustic_backward_velocity(float *d_vz, float *d_vx,
                                           float *d_szz, float *d_ave_Byc_a,
                                           float *d_ave_Byc_b, int nz, int nx,
                                           float dt, float dz, float dx,
                                           int npml, int npad);

__global__ void acoustic_backward_pressure(float *d_vz, float *d_vx,
                                           float *d_szz, float *d_Lambda,
                                           int nz, int nx, float dt, float dz,
                                           float dx, int npml, int npad);

__global__ void acoustic_adjoint_velocity(
    float *d_vz, float *d_vx, float *d_szz, float *d_mem_dvz_dz,
    float *d_mem_dvx_dx, float *d_mem_dszz_dz, float *d_mem_dsxx_dx,
    float *d_Lambda, float *d_ave_Byc_a, float *d_ave_Byc_b, float *d_K_z_half,
    float *d_a_z_half, float *d_b_z_half, float *d_K_x_half, float *d_a_x_half,
    float *d_b_x_half, float *d_K_z, float *d_a_z, float *d_b_z, float *d_K_x,
    float *d_a_x, float *d_b_x, int nz, int nx, float dt, float dz, float dx,
    int npml, int npad);

__global__ void acoustic_adjoint_pressure(
    float *d_vz, float *d_vx, float *d_szz, float *d_mem_dvz_dz,
    float *d_mem_dvx_dx, float *d_mem_dszz_dz, float *d_mem_dsxx_dx,
    float *d_Lambda, float *d_ave_Byc_a, float *d_ave_Byc_b, float *d_K_z_half,
    float *d_a_z_half, float *d_b_z_half, float *d_K_x_half, float *d_a_x_half,
    float *d_b_x_half, float *d_K_z, float *d_a_z, float *d_b_z, float *d_K_x,
    float *d_a_x, float *d_b_x, int nz, int nx, float dt, float dz, float dx,
    int npml, int npad);

__global__ void image_vel_time(float *d_szz, float *d_szz_plusone,
                               float *d_szz_adj, int nz, int nx, float dt,
                               float dz, float dx, int npml, int npad,
                               float *d_Vp, float *d_Lambda, float *d_VpGrad);

// Elastic Kernels
__global__ void elastic_forward_velocity(
    float *d_vz, float *d_vx, float *d_szz, float *d_sxx, float *d_sxz,
    float *d_mem_dszz_dz, float *d_mem_dsxz_dx, float *d_mem_dsxz_dz,
    float *d_mem_dsxx_dx, float *d_ave_Byc_a, float *d_ave_Byc_b, float *d_K_z,
    float *d_a_z, float *d_b_z, float *d_K_z_half, float *d_a_z_half,
    float *d_b_z_half, float *d_K_x, float *d_a_x, float *d_b_x,
    float *d_K_x_half, float *d_a_x_half, float *d_b_x_half, int nz, int nx,
    float dt, float dz, float dx, int npml, int npad);

__global__ void elastic_forward_stress(
    float *d_vz, float *d_vx, float *d_szz, float *d_sxx, float *d_sxz,
    float *d_mem_dvz_dz, float *d_mem_dvz_dx, float *d_mem_dvx_dz,
    float *d_mem_dvx_dx, float *d_Lambda, float *d_Mu, float *d_ave_Mu,
    float *d_K_z, float *d_a_z, float *d_b_z, float *d_K_z_half,
    float *d_a_z_half, float *d_b_z_half, float *d_K_x, float *d_a_x,
    float *d_b_x, float *d_K_x_half, float *d_a_x_half, float *d_b_x_half,
    int nz, int nx, float dt, float dz, float dx, int npml, int npad);

__global__ void elastic_backward_velocity(float *d_vz, float *d_vx,
                                          float *d_szz, float *d_sxx,
                                          float *d_sxz, float *d_ave_Byc_a,
                                          float *d_ave_Byc_b, int nz, int nx,
                                          float dt, float dz, float dx,
                                          int npml, int npad, float *d_vz_adj,
                                          float *d_vx_adj, float *d_DenGrad);

__global__ void elastic_backward_stress(
    float *d_vz, float *d_vx, float *d_szz, float *d_sxx, float *d_sxz,
    float *d_Lambda, float *d_Mu, float *d_ave_Mu, int nz, int nx, float dt,
    float dz, float dx, int npml, int npad, float *d_szz_adj, float *d_sxx_adj,
    float *d_sxz_adj, float *d_LambdaGrad, float *d_MuGrad);

__global__ void elastic_adjoint_velocity(
    float *d_vz, float *d_vx, float *d_szz, float *d_sxx, float *d_sxz,
    float *d_mem_dszz_dz, float *d_mem_dsxz_dx, float *d_mem_dsxz_dz,
    float *d_mem_dsxx_dx, float *d_mem_dvz_dz, float *d_mem_dvz_dx,
    float *d_mem_dvx_dz, float *d_mem_dvx_dx, float *d_Lambda, float *d_Mu,
    float *d_ave_Mu, float *d_Den, float *d_ave_Byc_a, float *d_ave_Byc_b,
    float *d_K_z_half, float *d_a_z_half, float *d_b_z_half, float *d_K_x_half,
    float *d_a_x_half, float *d_b_x_half, float *d_K_z, float *d_a_z,
    float *d_b_z, float *d_K_x, float *d_a_x, float *d_b_x, int nz, int nx,
    float dt, float dz, float dx, int npml, int npad);

__global__ void elastic_adjoint_stress(
    float *d_vz, float *d_vx, float *d_szz, float *d_sxx, float *d_sxz,
    float *d_mem_dszz_dz, float *d_mem_dsxz_dx, float *d_mem_dsxz_dz,
    float *d_mem_dsxx_dx, float *d_mem_dvz_dz, float *d_mem_dvz_dx,
    float *d_mem_dvx_dz, float *d_mem_dvx_dx, float *d_Lambda, float *d_Mu,
    float *d_ave_Mu, float *d_Den, float *d_ave_Byc_a, float *d_ave_Byc_b,
    float *d_K_z_half, float *d_a_z_half, float *d_b_z_half, float *d_K_x_half,
    float *d_a_x_half, float *d_b_x_half, float *d_K_z, float *d_a_z,
    float *d_b_z, float *d_K_x, float *d_a_x, float *d_b_x, int nz, int nx,
    float dt, float dz, float dx, int npml, int npad);

// Wavefield reconstruction tools
__global__ void from_bnd(float *d_field, float *d_bnd, int nz, int nx,
                         int nzBnd, int nxBnd, int len_Bnd_vec, int nLayerStore,
                         int indT, int npml, int npad, int nt);

__global__ void to_bnd(float *d_field, float *d_bnd, int nz, int nx, int nzBnd,
                       int nxBnd, int len_Bnd_vec, int nLayerStore, int indT,
                       int npml, int npad, int nt);

// Source tools
__global__ void src_rec_gauss_amp(float *gauss_amp, int nz, int nx);

__global__ void add_source(float *d_szz, float *d_sxx, float amp, int nz,
                           int z_loc, int x_loc, float dt, float *gauss_amp);

__global__ void sub_source(float *d_szz, float *d_sxx, float amp, int nz,
                           int z_loc, int x_loc, float dt, float *gauss_amp);

__global__ void source_grad(float *d_szz_adj, float *d_sxx_adj, int nz,
                            float *d_StfGrad, int it, float dt, int z_src,
                            int x_src);

__global__ void minus_source(float *d_szz, float *d_sxx, float amp, int nz,
                             int z_loc, int x_loc, float dt, float *d_Vp);

float source_update(int nt, float dt, int nrec, float *d_obs, float *d_data_cal,
                    float *d_source, cuFloatComplex *d_coef);

void source_update_adj(int nt, float dt, int nrec, float *d_data,
                       float amp_ratio, cuFloatComplex *d_coef);

// Receiver tools

__global__ void record_geo(float *d_szz, float *d_sxx, float *d_vx, float *d_vz,
                           int nz, float *d_syn_pr, float *d_syn_vx,
                           float *d_syn_vz, int iShot, int it, int nt, int nrec,
                           int *d_z_rec, int *d_x_rec) ;

__global__ void record_das(float *d_vx, float *d_vz, int nz, float *d_syn_et,
                           int iShot, int it, int nt, int ndas, int *d_z_das,
                           int *d_x_das, float *d_das_wt_x, 
                           float *d_das_wt_z,float gl);


__global__ void record_adj(float *d_szz, float *d_sxx, int nz, float *d_data,
                           int iShot, int it, int nt, int nrec, int z_loc,
                           int x_loc);

__global__ void inject_geo(float *d_szz_adj, float *d_sxx_adj, float *d_vx_adj,
                           float *d_vz_adj, int nz, float *d_res_pr,
                           float *d_res_vx, float *d_res_vz,
                           int it, float dt, int nt, int nrec, int *d_z_rec,
                           int *d_x_rec, float weight_pr, float weight_vx,
                           float weight_vz);

__global__ void inject_das(float *d_vx_adj, float *d_vz_adj, int nz, 
                           float *d_res_et, int it, float dt, int nt, int ndas, 
                           int *d_z_das, int *d_x_das, float weight_et, 
                           float *d_das_wt_x, float *d_das_wt_z, 
                           float gl);

// Processing tools
__global__ void cuda_bp_filter1d(int nt, float dt, int nrec,
                                 cufftComplex *d_data_F, float f0, float f1,
                                 float f2, float f3);

__global__ void cuda_filter1d(int nf, int nrec, cuFloatComplex *d_data_F,
                              cuFloatComplex *d_coef);

__global__ void cuda_normalize(int nz, int nx, float *data, float factor);

__global__ void cuda_window(int nt, int nrec, float dt, float *d_win_start,
                            float *d_win_end, float ratio, float *data);

__global__ void cuda_window(int nt, int nrec, float dt, float ratio,
                            float *data);

__global__ void cuda_embed_crop(int nz, int nx, float *d_data, int nz_pad,
                                int nx_pad, float *d_data_pad, bool isEmbed);

__global__ void cuda_spectrum_update(int nf, int nrec, cuFloatComplex *d_obs_F,
                                     cuFloatComplex *d_data_cal_F,
                                     cuFloatComplex *d_source_F,
                                     cuFloatComplex *d_coef);

__global__ void cuda_find_absmax(int n, cuFloatComplex *data, float maxval);

__global__ void cuda_find_normfact(int nt, int nrec, float *data1, float *data2,
                                   float *normfact);

__global__ void cuda_normal_traces(int nt, int nrec, float *normfact,
                                   float *data);

void bp_filter1d(int nt, float dt, int nrec, float *d_data, float *filter);

float amp_ratio_comp(int n, float *d_obs, float *d_data_cal);

#endif