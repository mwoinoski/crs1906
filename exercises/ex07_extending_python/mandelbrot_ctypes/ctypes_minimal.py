from ctypes import Structure, c_double, cdll, POINTER, c_int, cast, pointer, byref

class ComplexStruct(Structure):
    _fields_ = [("real", c_double), ("imag", c_double)]

library_mod = cdll.LoadLibrary('calc_z_ser.dll')

# void calc_z_ser(struct complex *)
calc_z_ser = library_mod.calc_z_ser
calc_z_ser.argtypes = (POINTER(ComplexStruct), POINTER(c_double), c_int, c_int)
calc_z_ser.restype = None

array_len = 3
maxiter = 10
input_array = (ComplexStruct * array_len)()
output_array = (c_double * array_len)()

for i in range(array_len):
    input_array[i].real = i + 0.3
    input_array[i].imag = i + 0.6

# verify the array of COMPLEX is populated
for i in range(array_len):
    print('{}: ({}, {})'. format(i, input_array[i].real, input_array[i].imag))

calc_z_ser(input_array, output_array, array_len, maxiter)
output = list(output_array)
for elem in output:
    print(elem)
