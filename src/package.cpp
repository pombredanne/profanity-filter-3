// Copyright (c) Timur Iskhakov.
// Distributed under the terms of the MIT License.


#include <boost/python.hpp>
#include "str_set.hpp"


BOOST_PYTHON_MODULE(str_set) {
    boost::python::class_<StrSet>("StrSet", boost::python::init<std::string const &, bool>())
    .def("check_occurrence", &StrSet::check_occurrence)
    .def("empty", &StrSet::empty)
    ;
}
