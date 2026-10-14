#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include <cstring>
#include <string>
#include <vector>
#include <stdexcept>
#include "edflib.h"

namespace py = pybind11;

struct EdfHeader {
    int signals;
    double duration_sec;
    std::vector<std::string> labels;
    std::vector<double> sample_rates;
    std::vector<long long> samples_per_signal;
};

EdfHeader read_header(const std::string& path) {
    edflib_hdr_t hdr;
    int r = edfopen_file_readonly(path.c_str(), &hdr, EDFLIB_READ_ALL_ANNOTATIONS);
    if (r < 0) throw std::runtime_error("Не удалось открыть EDF, код: " + std::to_string(r));

    EdfHeader out;
    out.signals = hdr.edfsignals;
    out.duration_sec = static_cast<double>(hdr.file_duration) / EDFLIB_TIME_DIMENSION;

    for (int i = 0; i < hdr.edfsignals; ++i) {
        std::string lab(hdr.signalparam[i].label);
        while (!lab.empty() && lab.back() == ' ') lab.pop_back();
        out.labels.emplace_back(lab);
        double fs = (out.duration_sec > 0.0)
            ? static_cast<double>(hdr.signalparam[i].smp_in_file) / out.duration_sec
            : 0.0;
        out.sample_rates.push_back(fs);
        out.samples_per_signal.push_back(hdr.signalparam[i].smp_in_file);
    }
    edfclose_file(hdr.handle);
    return out;
}

py::array_t<double> read_signal(const std::string& path, int channel) {
    edflib_hdr_t hdr;
    int r = edfopen_file_readonly(path.c_str(), &hdr, EDFLIB_READ_ALL_ANNOTATIONS);
    if (r < 0) throw std::runtime_error("Не удалось открыть EDF, код: " + std::to_string(r));
    if (channel < 0 || channel >= hdr.edfsignals) {
        edfclose_file(hdr.handle);
        throw std::out_of_range("Канал вне диапазона: " + std::to_string(channel));
    }

    long long n = hdr.signalparam[channel].smp_in_file;
    std::vector<double> buf(n);
    int got = edfread_physical_samples(hdr.handle, channel, static_cast<int>(n), buf.data());
    edfclose_file(hdr.handle);

    if (got < 0) throw std::runtime_error("Ошибка чтения сэмплов, код: " + std::to_string(got));
    buf.resize(got);

    py::array_t<double> arr(got);
    std::memcpy(arr.mutable_data(), buf.data(), static_cast<size_t>(got) * sizeof(double));
    return arr;
}

PYBIND11_MODULE(ecg_native, m) {
    m.doc() = "Быстрый парсер EDF через EDFlib";
    py::class_<EdfHeader>(m, "EdfHeader")
        .def_readonly("signals", &EdfHeader::signals)
        .def_readonly("duration_sec", &EdfHeader::duration_sec)
        .def_readonly("labels", &EdfHeader::labels)
        .def_readonly("sample_rates", &EdfHeader::sample_rates)
        .def_readonly("samples_per_signal", &EdfHeader::samples_per_signal);
    m.def("read_header", &read_header, "Прочитать заголовок EDF");
    m.def("read_signal", &read_signal, "Прочитать канал (0-based) в numpy array");
}
