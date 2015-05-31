/**
 * corpus boost::python module
 */

// Copyright (c) Timur Iskhakov.
// Distributed under the terms of the MIT License.


#include <boost/python.hpp>
#include "corpus.hpp"

template <class _Exception>
void translate_exception(_Exception const &e) {
    // Use the Python 'C' API to set up an exception object
    PyErr_SetString(PyExc_RuntimeError, e.what());
}

BOOST_PYTHON_MODULE(corpus) {
    boost::python::class_<Corpus>(
        "Corpus",
        boost::python::init<
            std::string const &,
            std::string const &,
            std::string const &,
            boost::python::object
        >()
    )
    .def("proceed", &Corpus::proceed)
    ;

    boost::python::register_exception_translator<CorpusException>(&translate_exception<CorpusException>);
}
