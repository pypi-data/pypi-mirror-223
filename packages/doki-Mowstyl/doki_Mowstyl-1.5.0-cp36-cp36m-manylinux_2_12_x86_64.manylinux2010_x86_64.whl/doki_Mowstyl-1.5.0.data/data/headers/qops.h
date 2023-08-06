#pragma once
#ifndef QOPS_H_
#define QOPS_H_

#include "arraylist.h"
#include "funmatrix.h"
#include "qgate.h"
#include "qstate.h"
#include <Python.h>

unsigned char join (struct state_vector *r, struct state_vector *s1,
                    struct state_vector *s2);

unsigned char measure (struct state_vector *state, _Bool *result,
                       unsigned int target, struct state_vector *new_state,
                       REAL_TYPE roll);

REAL_TYPE
probability (struct state_vector *state, unsigned int target_id);

REAL_TYPE
get_global_phase (struct state_vector *state);

unsigned char collapse (struct state_vector *state, unsigned int id,
                        _Bool value, struct state_vector *new_state);

unsigned char apply_gate (struct state_vector *state, struct qgate *gate,
                          unsigned int *targets, unsigned int num_targets,
                          unsigned int *controls, unsigned int num_controls,
                          unsigned int *anticontrols,
                          unsigned int num_anticontrols,
                          struct state_vector *new_state);

unsigned char
copy_and_index (struct state_vector *state, struct state_vector *new_state,
                unsigned int *controls, unsigned int num_controls,
                unsigned int *anticontrols, unsigned int num_anticontrols,
                REAL_TYPE *norm_const, struct array_list_e *not_copy);

unsigned char
calculate_empty (struct state_vector *state, struct qgate *gate,
                 unsigned int *targets, unsigned int num_targets,
                 unsigned int *controls, unsigned int num_controls,
                 unsigned int *anticontrols, unsigned int num_anticontrols,
                 struct state_vector *new_state, struct array_list_e *not_copy,
                 REAL_TYPE *norm_const);

struct FMatrix *
apply_gate_fmat (PyObject *state_capsule, PyObject *gate_capsule,
                 unsigned int *targets, unsigned int num_targets,
                 unsigned int *controls, unsigned int num_controls,
                 unsigned int *anticontrols, unsigned int num_anticontrols);

struct FMatrix *density_matrix (PyObject *state_capsule);

#endif /* QOPS_H_ */
