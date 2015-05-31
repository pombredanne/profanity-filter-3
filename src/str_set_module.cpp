/**
 * str_set boost::python module
 */

// Copyright (c) Timur Iskhakov.
// Distributed under the terms of the MIT License.


#include <boost/python.hpp>
#include "str_set.hpp"


BOOST_PYTHON_MODULE(str_set) {
    boost::python::class_<StrSet>("StrSet", boost::python::init<std::string const &>())
    .def("check_occurrence", &StrSet::check_occurrence_python)
    .def("empty", &StrSet::empty)
    ;
}
