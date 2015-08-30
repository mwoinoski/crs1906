#include <stdio.h>
#include "Python.h"
#include "calc_z_ser.h"

/* int calc_z_ser(struct complex * q, int * output, int len_q, int maxiter) */
/*
 * TODO: note the definition of the py_calc_z_ser() function.
 * T
   (no code change required) */
static PyObject *py_calc_z_ser(PyObject *self, PyObject *args) {
  PyObject *q, *output;
  int len_q, maxiter, result = 0;
  Py_buffer q_buffer, output_buffer;

  /* Get the arguments: two arrays (two Objects) and two int  */
  if (!PyArg_ParseTuple(args, "OOii", &q, &output, &len_q, &maxiter)) {
    return NULL;
  }

  /* Attempt to extract buffer information from q */
  if (PyObject_GetBuffer(q, &q_buffer,
                         PyBUF_ANY_CONTIGUOUS | PyBUF_FORMAT) == -1) {
    return NULL;
  }

  if (q_buffer.ndim != 1) {
    PyErr_SetString(PyExc_TypeError,
                    "First arg must be a 1-dimensional array of complex");
    PyBuffer_Release(&q_buffer);
    return NULL;
  }

  /* Attempt to extract buffer information from output_buffer */
  if (PyObject_GetBuffer(output, &output_buffer,
                         PyBUF_ANY_CONTIGUOUS | PyBUF_FORMAT) == -1) {
    return NULL;
  }

  if (output_buffer.ndim != 1) {
    PyErr_SetString(PyExc_TypeError,
                    "Second arg must be a 1-dimensional array of int");
    PyBuffer_Release(&output_buffer);
    return NULL;
  }

  /* Check the type of items in the array */
  if (strcmp(output_buffer.format, "i") != 0) {
    PyErr_SetString(PyExc_TypeError, "Second arg must be an array of int");
    PyBuffer_Release(&output_buffer);
    return NULL;
  }

  /* Pass the raw buffers to the C function */
  result = calc_z_ser(q_buffer.buf, output_buffer.buf, len_q, maxiter);

  /* Indicate we're done working with the buffers */
  PyBuffer_Release(&q_buffer);
  PyBuffer_Release(&output_buffer);
  return Py_BuildValue("i", result);
}


/* Module method table */
static PyMethodDef CalcZSerMethods[] = {
  {"calc_z_ser", py_calc_z_ser, METH_VARARGS, "Generate Mandelbrot series"},
  { NULL, NULL, 0, NULL}
};

/* Module structure */
static struct PyModuleDef calc_z_ser_ext_mod = {
  PyModuleDef_HEAD_INIT,
  "calc_z_ser_ext_mod",           /* name of module */
  "calc_z_ser extension module",  /* Doc string (may be NULL) */
  -1,                             /* Size of per-interpreter state or -1 */
  CalcZSerMethods                 /* Method table */
};

/* Module initialization function */
PyMODINIT_FUNC
PyInit_calc_z_ser_ext_mod(void) {
  return PyModule_Create(&calc_z_ser_ext_mod);
}
