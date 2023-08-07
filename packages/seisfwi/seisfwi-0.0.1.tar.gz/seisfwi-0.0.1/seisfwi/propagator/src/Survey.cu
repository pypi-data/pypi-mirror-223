// Dongzhuo Li 05/13/2018
// Modified by Dongzhuo Li 06/25/2018
#include "Survey.h"
#include "utils.h"
#include <cuda_runtime.h>
#include <fstream>
#include <iostream>
#include <string>

#define stf(iShot, it) stf[(iShot) * (nt) + (it)] // row-major

using namespace std;
using namespace rapidjson;

Survey::Survey() {
  cout << "ERROR: You need to input parameter!" << endl;
  exit(1);
}

Survey::Survey(Parameter &para, const bool with_adj, const bool with_residual,
               const float *stf, int group_size, const int *shot_ids) {

  // default values
  string line;
  ifstream survery_file;

  // open survey file and read in the survey info
  survery_file.open(para.survey_fname());

  if (!survery_file.is_open()) {
    cout << "Error opening survey file" << endl;
    exit(1);
  }

  getline(survery_file, line);
  survery_file.close();

  Document json_survery;
  json_survery.Parse<0>(line.c_str());
  assert(json_survery.IsObject());

  // surver mode
  with_adj_ = with_adj;
  with_residual_ = with_residual;
  if_win_ = para.if_win();

  int nrec = 0;
  int ndas = 0;
  int z_src = 10;
  int x_src = 10;
  int nt = para.nt();
  int npml = para.npml();
  float dt = para.dt();

  int *h_z_rec = nullptr;
  int *h_x_rec = nullptr;
  int *h_z_das = nullptr;
  int *h_x_das = nullptr;
  
  float *h_win_start = nullptr; // for selected window
  float *h_win_end = nullptr;   // for selected window
  float *h_x_weight = nullptr;   // for das weighting
  float *h_z_weight = nullptr;   // for das weighting
  float *h_source = nullptr;

  // syn data: pr, vx, vz, et components
  float *h_syn_pr = nullptr;
  float *h_syn_vx = nullptr;
  float *h_syn_vz = nullptr;
  float *h_syn_et = nullptr;
  // obs data: pr, vx, vz, et components
  float *h_obs_pr = nullptr;
  float *h_obs_vx = nullptr;
  float *h_obs_vz = nullptr;
  float *h_obs_et = nullptr;
  // res data: pr, vx, vz, et components
  float *h_res_pr = nullptr;
  float *h_res_vx = nullptr;
  float *h_res_vz = nullptr;
  float *h_res_et = nullptr;
  // adj data: pr components since explosive source
  float *h_adj_pr = nullptr;

  // for shot number small than 99999
  char thisShot[10];

  // device pointers
  int *d_z_rec, *d_x_rec;
  int *d_z_das, *d_x_das;
  float *d_source;
  float *d_win_start, *d_win_end;
  float *d_x_weight, *d_z_weight;


  // get the source number
  assert(json_survery.HasMember("nShots"));
  assert(json_survery["nShots"].IsInt());
  nShots = json_survery["nShots"].GetInt();

  // get the guage length
  assert(json_survery.HasMember("gauge_length"));
  assert(json_survery["gauge_length"].IsFloat());
  gl = json_survery["gauge_length"].GetFloat();

  CHECK(cudaMalloc((void **)&d_coef, (nt + 1) * sizeof(cuFloatComplex)));

  for (int i = 0; i < group_size; i++) {

    // get the source positions: z_src, x_src
    strcpy(thisShot, ("shot" + to_string(shot_ids[i])).c_str());

    assert(json_survery[thisShot].HasMember("z_src"));
    assert(json_survery[thisShot]["z_src"].IsInt());
    z_src = json_survery[thisShot]["z_src"].GetInt() + npml;
    vec_z_src.push_back(z_src);

    assert(json_survery[thisShot].HasMember("x_src"));
    assert(json_survery[thisShot]["x_src"].IsInt());
    x_src = json_survery[thisShot]["x_src"].GetInt() + npml;
    vec_x_src.push_back(x_src);

    // get the number of rec for each shot
    assert(json_survery[thisShot].HasMember("nrec"));
    assert(json_survery[thisShot]["nrec"].IsInt());
    nrec = json_survery[thisShot]["nrec"].GetInt();
    vec_nrec.push_back(nrec);
    h_z_rec = new int[nrec];
    h_x_rec = new int[nrec];

    // read in the receiver positions for this shot: z_rec, x_rec
    assert(json_survery[thisShot].HasMember("z_rec"));
    assert(json_survery[thisShot]["z_rec"].IsArray());
    const Value &js_z_rec = json_survery[thisShot]["z_rec"];
    for (SizeType ii = 0; ii < js_z_rec.Size(); ii++) {
      h_z_rec[ii] = js_z_rec[ii].GetInt() + npml;
    }

    assert(json_survery[thisShot].HasMember("x_rec"));
    assert(json_survery[thisShot]["x_rec"].IsArray());
    const Value &js_x_rec = json_survery[thisShot]["x_rec"];
    for (SizeType ii = 0; ii < js_x_rec.Size(); ii++) {
      h_x_rec[ii] = js_x_rec[ii].GetInt() + npml;
    }

    // get receiver z positions for each shot
    CHECK(cudaMalloc((void **)&d_z_rec, nrec * sizeof(int)));
    CHECK(cudaMemcpy(d_z_rec, h_z_rec, nrec * sizeof(int), cudaMemcpyHostToDevice));
    d_vec_z_rec.push_back(d_z_rec);

    // get receiver x positions for each shot
    CHECK(cudaMalloc((void **)&d_x_rec, nrec * sizeof(int)));
    CHECK(cudaMemcpy(d_x_rec, h_x_rec, nrec * sizeof(int), cudaMemcpyHostToDevice));
    d_vec_x_rec.push_back(d_x_rec);

  
    // get the number of DAS channel for each shot
    assert(json_survery[thisShot].HasMember("ndas"));
    assert(json_survery[thisShot]["ndas"].IsInt());
    ndas = json_survery[thisShot]["ndas"].GetInt();
    vec_ndas.push_back(ndas);
    h_z_das = new int[ndas];
    h_x_das = new int[ndas];
  
    // read in the DAS channel positions for this shot: z_das, x_das
    assert(json_survery[thisShot].HasMember("z_das"));
    assert(json_survery[thisShot]["z_das"].IsArray());
    const Value &js_z_das = json_survery[thisShot]["z_das"];
    for (SizeType ii = 0; ii < js_z_das.Size(); ii++) {
      h_z_das[ii] = js_z_das[ii].GetInt() + npml;
    }

    assert(json_survery[thisShot].HasMember("x_das"));
    assert(json_survery[thisShot]["x_das"].IsArray());
    const Value &js_x_das = json_survery[thisShot]["x_das"];
    for (SizeType ii = 0; ii < js_x_das.Size(); ii++) {
      h_x_das[ii] = js_x_das[ii].GetInt() + npml;
    }

    // get DAS z positions for each shot
    CHECK(cudaMalloc((void **)&d_z_das, ndas * sizeof(int)));
    CHECK(cudaMemcpy(d_z_das, h_z_das, ndas * sizeof(int), cudaMemcpyHostToDevice));
    d_vec_z_das.push_back(d_z_das);

    // get DAS x positions for each shot
    CHECK(cudaMalloc((void **)&d_x_das, ndas * sizeof(int)));
    CHECK(cudaMemcpy(d_x_das, h_x_das, ndas * sizeof(int), cudaMemcpyHostToDevice));
    d_vec_x_das.push_back(d_x_das);
    

    // get weights: the weight is for x component
    h_x_weight = new float[ndas];
    assert(json_survery[thisShot].HasMember("das_wt_x"));
    assert(json_survery[thisShot]["das_wt_x"].IsArray());
    const Value &js_weights = json_survery[thisShot]["das_wt_x"];
    for (SizeType ii = 0; ii < js_weights.Size(); ii++) {
      h_x_weight[ii] = js_weights[ii].GetDouble();
    }
    CHECK(cudaMalloc((void **)&d_x_weight, ndas * sizeof(float)));
    CHECK(cudaMemcpy(d_x_weight, h_x_weight, ndas * sizeof(float), cudaMemcpyHostToDevice));
    d_vec_das_wt_x.push_back(d_x_weight);
    delete[] h_x_weight;

    // get weights: the weight is for z component
    h_z_weight = new float[ndas];
    assert(json_survery[thisShot].HasMember("das_wt_z"));
    assert(json_survery[thisShot]["das_wt_z"].IsArray());
    const Value &js_weights2 = json_survery[thisShot]["das_wt_z"];
    for (SizeType ii = 0; ii < js_weights2.Size(); ii++) {
      h_z_weight[ii] = js_weights2[ii].GetDouble();
    }
    CHECK(cudaMalloc((void **)&d_z_weight, ndas * sizeof(float)));
    CHECK(cudaMemcpy(d_z_weight, h_z_weight, ndas * sizeof(float), cudaMemcpyHostToDevice));
    d_vec_das_wt_z.push_back(d_z_weight);
    delete[] h_z_weight;


    // get the source time function for each shot
    h_source = new float[nt];
    for (int it = 0; it < nt; it++) {
      h_source[it] = stf(shot_ids[i], it);
    }

    CHECK(cudaMalloc((void **)&d_source, nt * sizeof(float)));
    CHECK(cudaMemcpy(d_source, h_source, nt * sizeof(float), cudaMemcpyHostToDevice));
    cuda_window<<<(nt + 31) / 32, 32>>>(nt, 1, dt, 0.001, d_source);

    // if (para.if_filter()) {
    //   bp_filter1d(nt, dt, 1, d_source, para.filter());
    // }

    CHECK(cudaMemcpy(h_source, d_source, nt * sizeof(float), cudaMemcpyDeviceToHost));
    vec_source.push_back(h_source);
    d_vec_source.push_back(d_source);

    // get the window for each shot
    if (if_win_) {
      h_win_start = new float[nrec];
      h_win_end = new float[nrec];

      // window start
      assert(json_survery[thisShot].HasMember("win_start"));
      assert(json_survery[thisShot]["win_start"].IsArray());
      const Value &js_win_start = json_survery[thisShot]["win_start"];
      for (SizeType ii = 0; ii < js_win_start.Size(); ii++) {
        h_win_start[ii] = js_win_start[ii].GetDouble();
      }

      // window end
      assert(json_survery[thisShot].HasMember("win_end"));
      assert(json_survery[thisShot]["win_end"].IsArray());
      const Value &js_win_end = json_survery[thisShot]["win_end"];
      for (SizeType ii = 0; ii < js_win_end.Size(); ii++) {
        h_win_end[ii] = js_win_end[ii].GetDouble();
      }

      // push to device
      CHECK(cudaMalloc((void **)&d_win_start, nrec * sizeof(float)));
      CHECK(cudaMemcpy(d_win_start, h_win_start, nrec * sizeof(float), cudaMemcpyHostToDevice));
      d_vec_win_start.push_back(d_win_start);

      CHECK(cudaMalloc((void **)&d_win_end, nrec * sizeof(float)));
      CHECK(cudaMemcpy(d_win_end, h_win_end, nrec * sizeof(float), cudaMemcpyHostToDevice));
      d_vec_win_end.push_back(d_win_end);

      delete[] h_win_start;
      delete[] h_win_end;
    }


    // Initialize the host side data cube for pr, vx, vz and et components
    cudaHostAlloc((void **)&h_syn_pr, nt * nrec * sizeof(float), cudaHostAllocDefault);
    initialArray(h_syn_pr, nt * nrec, 0.0);
    vec_syn_pr.push_back(h_syn_pr);

    cudaHostAlloc((void **)&h_syn_vx, nt * nrec * sizeof(float), cudaHostAllocDefault);
    initialArray(h_syn_vx, nt * nrec, 0.0);
    vec_syn_vx.push_back(h_syn_vx);

    cudaHostAlloc((void **)&h_syn_vz, nt * nrec * sizeof(float), cudaHostAllocDefault);
    initialArray(h_syn_vz, nt * nrec, 0.0);
    vec_syn_vz.push_back(h_syn_vz);

    cudaHostAlloc((void **)&h_syn_et, nt * ndas * sizeof(float), cudaHostAllocDefault);
    initialArray(h_syn_et, nt * ndas, 0.0);
    vec_syn_et.push_back(h_syn_et);

    if (with_residual_) {
      // initialize the host side observed data cube for pr, vx, vz and et
      // components
      cudaHostAlloc((void **)&h_obs_pr, nt * nrec * sizeof(float), cudaHostAllocDefault);
      initialArray(h_obs_pr, nt * nrec, 0.0);
      vec_obs_pr.push_back(h_obs_pr);

      cudaHostAlloc((void **)&h_obs_vx, nt * nrec * sizeof(float), cudaHostAllocDefault);
      initialArray(h_obs_vx, nt * nrec, 0.0);
      vec_obs_vx.push_back(h_obs_vx);

      cudaHostAlloc((void **)&h_obs_vz, nt * nrec * sizeof(float), cudaHostAllocDefault);
      initialArray(h_obs_vz, nt * nrec, 0.0);
      vec_obs_vz.push_back(h_obs_vz);

      cudaHostAlloc((void **)&h_obs_et, nt * ndas * sizeof(float), cudaHostAllocDefault);
      initialArray(h_obs_et, nt * ndas, 0.0);
      vec_obs_et.push_back(h_obs_et);

      // initialize the host side data residual data cube for pr, vx, vz and et
      // components
      cudaHostAlloc((void **)&h_res_pr, nt * nrec * sizeof(float), cudaHostAllocDefault);
      initialArray(h_res_pr, nt * nrec, 0.0);
      vec_res_pr.push_back(h_res_pr);

      cudaHostAlloc((void **)&h_res_vx, nt * nrec * sizeof(float), cudaHostAllocDefault);
      initialArray(h_res_vx, nt * nrec, 0.0);
      vec_res_vx.push_back(h_res_vx);

      cudaHostAlloc((void **)&h_res_vz, nt * nrec * sizeof(float), cudaHostAllocDefault);
      initialArray(h_res_vz, nt * nrec, 0.0);
      vec_res_vz.push_back(h_res_vz);

      cudaHostAlloc((void **)&h_res_et, nt * ndas * sizeof(float), cudaHostAllocDefault);
      initialArray(h_res_et, nt * ndas, 0.0);
      vec_res_et.push_back(h_res_et);
    }

    if (with_adj) {
      cudaHostAlloc((void **)&h_adj_pr, nt * 1 * sizeof(float), cudaHostAllocDefault);
      initialArray(h_adj_pr, nt * 1, 0.0);
      vec_adj_pr.push_back(h_adj_pr);
    }

  }
}

Survey::~Survey() {

  for (int i = 0; i < d_vec_x_rec.size(); i++) {
    CHECK(cudaFree(d_vec_z_rec.at(i)));
    CHECK(cudaFree(d_vec_x_rec.at(i)));
  }

  for (int i = 0; i < d_vec_x_das.size(); i++) {
    CHECK(cudaFree(d_vec_z_das.at(i)));
    CHECK(cudaFree(d_vec_x_das.at(i)));
  }

  for (int i = 0; i < vec_source.size(); i++) {
    delete[] vec_source.at(i);
    CHECK(cudaFree(d_vec_source.at(i)));
  }

  // free forward record data
  for (int i = 0; i < vec_syn_pr.size(); i++) {
    CHECK(cudaFreeHost(vec_syn_pr.at(i)));
    CHECK(cudaFreeHost(vec_syn_vx.at(i)));
    CHECK(cudaFreeHost(vec_syn_vz.at(i)));
  }

  for (int i = 0; i < vec_syn_et.size(); i++) {
    CHECK(cudaFreeHost(vec_syn_et.at(i)));
  }

  // free residual record data
  if (with_residual_) {
    for (int i = 0; i < vec_obs_pr.size(); i++) {
      CHECK(cudaFreeHost(vec_obs_pr.at(i)));
      CHECK(cudaFreeHost(vec_obs_vx.at(i)));
      CHECK(cudaFreeHost(vec_obs_vz.at(i)));
      CHECK(cudaFreeHost(vec_res_pr.at(i)));
      CHECK(cudaFreeHost(vec_res_vx.at(i)));
      CHECK(cudaFreeHost(vec_res_vz.at(i)));
    }
    for (int i = 0; i < vec_obs_et.size(); i++) {
      CHECK(cudaFreeHost(vec_obs_et.at(i)));
      CHECK(cudaFreeHost(vec_res_et.at(i)));
    }
  }

  // free adjoint record data
  if (with_adj_) {
    for (int i = 0; i < vec_adj_pr.size(); i++) {
      CHECK(cudaFreeHost(vec_adj_pr.at(i)));
    }
  }

  // free windowing data
  if (if_win_) {
    for (int i = 0; i < d_vec_win_start.size(); i++) {
      CHECK(cudaFree(d_vec_win_start.at(i)));
      CHECK(cudaFree(d_vec_win_end.at(i)));
    }
  }

  // free source weight data
  for (int i = 0; i < d_vec_das_wt_x.size(); i++) {
    CHECK(cudaFree(d_vec_das_wt_x.at(i)));
    CHECK(cudaFree(d_vec_das_wt_z.at(i)));
  }

  CHECK(cudaFree(d_coef));
}