#include "Python.h"
#include "primes.h"

/* int is_prime(int) */
static PyObject *py_is_prime(PyObject *self, PyObject *args) {
  int x, result;

  if (!PyArg_ParseTuple(args, "i", &x)) { /* param list is one int */
    return NULL;
  }
  result = is_prime(x);
  return Py_BuildValue("i", result); /* result is an int */
}

/* int primes_c(int, int *) */
static PyObject *py_primes_c(PyObject *self, PyObject *args) {
  int howmany;
  PyObject *bufobj;
  Py_buffer view;
  double result;
  /* Get the howmany param and the passed Python object (int and Object) */
  if (!PyArg_ParseTuple(args, "iO", &howmany, &bufobj)) {
    return NULL;
  }

  /* Attempt to extract buffer information from it */
  if (PyObject_GetBuffer(bufobj, &view,
                         PyBUF_ANY_CONTIGUOUS | PyBUF_FORMAT) == -1) {
    return NULL;
  }

  if (view.ndim != 1) {
    PyErr_SetString(PyExc_TypeError, "Expected a 1-dimensional array");
    PyBuffer_Release(&view);
    return NULL;
  }

  /* Check the type of items in the array */
  if (strcmp(view.format, "i") != 0) {
    PyErr_SetString(PyExc_TypeError, "Expected an array of int");
    PyBuffer_Release(&view);
    return NULL;
  }

  /* Pass the raw buffer to the C function */
  result = primes_c(howmany, view.buf);

  /* Indicate we're done working with the buffer */
  PyBuffer_Release(&view);
  return Py_BuildValue("i", result);
}


/* Module method table */
static PyMethodDef PrimesMethods[] = {
  {"is_prime",  py_is_prime, METH_VARARGS, "Test for prime number"},
  {"primes_c", py_primes_c, METH_VARARGS, "Generate table of primes"},
  { NULL, NULL, 0, NULL}
};

/* Module structure */
static struct PyModuleDef primes_ext_mod = {
  PyModuleDef_HEAD_INIT,
  "primes_ext_mod",           /* name of module */
  "Primes extension module",  /* Doc string (may be NULL) */
  -1,                         /* Size of per-interpreter state or -1 */
  PrimesMethods               /* Method table */
};

/* Module initialization function */
PyMODINIT_FUNC
PyInit_primes_ext_mod(void) {
  return PyModule_Create(&primes_ext_mod);
}
