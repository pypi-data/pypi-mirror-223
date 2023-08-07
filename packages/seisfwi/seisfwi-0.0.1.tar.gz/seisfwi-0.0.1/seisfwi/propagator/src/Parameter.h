// Dongzhuo Li 04/22/2018]
// Modify by Haipeng Li 06/25/2023
#ifndef PARAMETER_H__
#define PARAMETER_H__

#include "utils.h"
#include <string>

class Parameter {
private:
  int nz_;
  int nx_;
  int nt_;
  int npml_;
  int npad_;
  float dz_;
  float dx_;
  float dt_;
  float f0_;
  float weight_pr_;
  float weight_vx_;
  float weight_vz_;
  float weight_et_;
  float filter_[4];
  std::string survey_fname_;
  std::string data_dir_name_;
  std::string scratch_dir_name_;

  bool if_win_ = false;
  bool if_src_update_ = false;
  bool if_filter_ = false;
  bool if_save_scratch_ = false;
  bool if_cross_misfit_ = false;

public:
  Parameter();
  Parameter(const std::string &para_fname);
  ~Parameter();

  int nz() const { return nz_; }
  int nx() const { return nx_; }
  int nt() const { return nt_; }
  int npml() const { return npml_; }
  int npad() const { return npad_; }

  float dz() const { return dz_; }
  float dx() const { return dx_; }
  float dt() const { return dt_; }
  float f0() const { return f0_; }
  float weight_pr() const { return weight_pr_; }
  float weight_vx() const { return weight_vx_; }
  float weight_vz() const { return weight_vz_; }
  float weight_et() const { return weight_et_; }
  float *filter() { return filter_; }

  std::string survey_fname() const { return survey_fname_; }
  std::string data_dir_name() const { return data_dir_name_; }
  std::string scratch_dir_name() const { return scratch_dir_name_; }

  bool if_win() const { return if_win_; }
  bool if_src_update() const { return if_src_update_; }
  bool if_filter() const { return if_filter_; }
  bool if_save_scratch() const { return if_save_scratch_; }
  bool if_cross_misfit() const { return if_cross_misfit_; }
};

#endif