// Dongzhuo Li 05/13/2018
// Modify by Haipeng Li 06/25/2023
#ifndef SURVEY_H__
#define SURVEY_H__

#include <vector>
#include "Parameter.h"
#include "utils.h"

class Survey
{
private:
  bool with_adj_;
  bool with_residual_;
  bool if_win_;

public:
  std::vector<int> vec_z_src;
  std::vector<int> vec_x_src;
  std::vector<int> vec_nrec;
  std::vector<int> vec_ndas;
  std::vector<int *> d_vec_z_rec;
  std::vector<int *> d_vec_x_rec;
  std::vector<int *> d_vec_z_das;
  std::vector<int *> d_vec_x_das;
  std::vector<float *> d_vec_das_wt_x;   // device side weights for DAS x component
  std::vector<float *> d_vec_das_wt_z;   // device side weights for DAS z component
  std::vector<float *> d_vec_win_start; // device side window
  std::vector<float *> d_vec_win_end;   // device side window
  std::vector<float *> d_vec_source;    // device side source
  std::vector<float *> vec_source;      // host side source
  std::vector<float *> vec_syn_pr;      // host side synthetic data: pr
  std::vector<float *> vec_syn_vx;      // host side synthetic data: vx
  std::vector<float *> vec_syn_vz;      // host side synthetic data: vz
  std::vector<float *> vec_syn_et;      // host side synthetic data: et
  std::vector<float *> vec_obs_pr;      // host side observed data: pr
  std::vector<float *> vec_obs_vx;      // host side observed data: vx
  std::vector<float *> vec_obs_vz;      // host side observed data: vz
  std::vector<float *> vec_obs_et;      // host side observed data: et
  std::vector<float *> vec_res_pr;      // host side data residual: pr
  std::vector<float *> vec_res_vx;      // host side data residual: vx
  std::vector<float *> vec_res_vz;      // host side data residual: vz
  std::vector<float *> vec_res_et;      // host side data residual: et
  std::vector<float *> vec_adj_pr;      // host side adjoint data: pr

  cuFloatComplex *d_coef;
  int nShots;
  float gl;

  Survey();
  Survey(Parameter &para);
  Survey(Parameter &para, const bool with_adj, const bool with_residual,
         const float *stf, int group_size, const int *shot_ids);
  Survey(const Survey &) = delete;
  Survey &operator=(const Survey &) = delete;
  ~Survey();
};

#endif