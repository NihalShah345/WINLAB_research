#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: amangrandhi
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import blocks
from gnuradio import channels
from gnuradio.filter import firdes
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
import sip
import time
import threading



class OFDM_Signal_Analyzer(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "OFDM_Signal_Analyzer")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.variable_function_probe_signal = variable_function_probe_signal = 0
        self.variable_function_probe_noise = variable_function_probe_noise = 0
        self.snr = snr = (variable_function_probe_signal-variable_function_probe_noise)
        self.signalPowerLabel = signalPowerLabel = variable_function_probe_signal
        self.samp_rate = samp_rate = 100000
        self.packet_len = packet_len = 50
        self.noise_voltage = noise_voltage = 0.1
        self.noisePowerLabel = noisePowerLabel = variable_function_probe_noise
        self.len_tag_key = len_tag_key = "packet_len"
        self.intSize = intSize = 250000
        self.freq_offset = freq_offset = 0
        self.fft_len = fft_len = 64
        self.cf = cf = 90.9e6

        ##################################################
        # Blocks
        ##################################################

        self.probeSignalPowerNoise = blocks.probe_signal_f()
        self.probeSignalPower = blocks.probe_signal_f()
        self._noise_voltage_range = qtgui.Range(0, 1, .01, 0.1, 200)
        self._noise_voltage_win = qtgui.RangeWidget(self._noise_voltage_range, self.set_noise_voltage, "Noise Amplitude", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._noise_voltage_win)
        self._freq_offset_range = qtgui.Range(-3, 3, .01, 0, 200)
        self._freq_offset_win = qtgui.RangeWidget(self._freq_offset_range, self.set_freq_offset, "Frequency Offset (Multiples of Sub-carrier spacing)", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._freq_offset_win)
        def _variable_function_probe_signal_probe():
          while True:

            val = self.probeSignalPower.level()
            try:
              try:
                self.doc.add_next_tick_callback(functools.partial(self.set_variable_function_probe_signal,val))
              except AttributeError:
                self.set_variable_function_probe_signal(val)
            except AttributeError:
              pass
            time.sleep(1.0 / (10))
        _variable_function_probe_signal_thread = threading.Thread(target=_variable_function_probe_signal_probe)
        _variable_function_probe_signal_thread.daemon = True
        _variable_function_probe_signal_thread.start()
        def _variable_function_probe_noise_probe():
          while True:

            val = self.probeSignalPowerNoise.level()
            try:
              try:
                self.doc.add_next_tick_callback(functools.partial(self.set_variable_function_probe_noise,val))
              except AttributeError:
                self.set_variable_function_probe_noise(val)
            except AttributeError:
              pass
            time.sleep(1.0 / (10))
        _variable_function_probe_noise_thread = threading.Thread(target=_variable_function_probe_noise_probe)
        _variable_function_probe_noise_thread.daemon = True
        _variable_function_probe_noise_thread.start()
        self._snr_tool_bar = Qt.QToolBar(self)

        if None:
            self._snr_formatter = None
        else:
            self._snr_formatter = lambda x: eng_notation.num_to_str(x)

        self._snr_tool_bar.addWidget(Qt.QLabel("SNR (dB): "))
        self._snr_label = Qt.QLabel(str(self._snr_formatter(self.snr)))
        self._snr_tool_bar.addWidget(self._snr_label)
        self.top_grid_layout.addWidget(self._snr_tool_bar, 0, 6, 1, 3)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(6, 9):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._signalPowerLabel_tool_bar = Qt.QToolBar(self)

        if None:
            self._signalPowerLabel_formatter = None
        else:
            self._signalPowerLabel_formatter = lambda x: eng_notation.num_to_str(x)

        self._signalPowerLabel_tool_bar.addWidget(Qt.QLabel("Signal Power (dBfs): "))
        self._signalPowerLabel_label = Qt.QLabel(str(self._signalPowerLabel_formatter(self.signalPowerLabel)))
        self._signalPowerLabel_tool_bar.addWidget(self._signalPowerLabel_label)
        self.top_grid_layout.addWidget(self._signalPowerLabel_tool_bar, 0, 0, 1, 3)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0_0 = qtgui.freq_sink_c(
            8192, #size
            window.WIN_FLATTOP, #wintype
            cf, #fc
            samp_rate, #bw
            "", #name
            3,
            None # parent
        )
        self.qtgui_freq_sink_x_0_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_0.set_y_axis((-110), (-10))
        self.qtgui_freq_sink_x_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0.enable_grid(True)
        self.qtgui_freq_sink_x_0_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0_0.set_fft_window_normalized(False)



        labels = ['RF Spectrum', 'Filtered Signal Spectrum', 'Filtered Noise Spectrum', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["black", "green", "red", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(3):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_0_win, 1, 0, 5, 10)
        for r in range(1, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 10):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._noisePowerLabel_tool_bar = Qt.QToolBar(self)

        if None:
            self._noisePowerLabel_formatter = None
        else:
            self._noisePowerLabel_formatter = lambda x: eng_notation.num_to_str(x)

        self._noisePowerLabel_tool_bar.addWidget(Qt.QLabel("Noise Power (dBfs): "))
        self._noisePowerLabel_label = Qt.QLabel(str(self._noisePowerLabel_formatter(self.noisePowerLabel)))
        self._noisePowerLabel_tool_bar.addWidget(self._noisePowerLabel_label)
        self.top_grid_layout.addWidget(self._noisePowerLabel_tool_bar, 0, 3, 1, 3)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(3, 6):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.filter_fft_low_pass_filter_0 = filter.fft_filter_ccc(1, firdes.low_pass(1, 275e3, 50e3, 5e3, window.WIN_BLACKMAN, 6.76), 1)
        self.digital_ofdm_tx_0_0 = digital.ofdm_tx(
            fft_len=fft_len,
            cp_len=(fft_len//4),
            packet_length_tag_key=len_tag_key,
            occupied_carriers=((-27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -6, -4, -3, -2, -1, 1, 2, 3, 4, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27),),
            pilot_carriers=((-7,-5,5,6),),
            pilot_symbols=((-1,1,-1,1),),
            sync_word1=None,
            sync_word2=None,
            bps_header=1,
            bps_payload=2,
            rolloff=0,
            debug_log=False,
            scramble_bits=False)
        self.channels_channel_model_0 = channels.channel_model(
            noise_voltage=noise_voltage,
            frequency_offset=(freq_offset * 1.0/fft_len),
            epsilon=1.0,
            taps=[1.0 + 1.0j],
            noise_seed=0,
            block_tags=True)
        self.blocks_vector_source_x_0 = blocks.vector_source_b(range(packet_len), True, 1, ())
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, packet_len, len_tag_key)
        self.blocks_nlog10_ff_0_0 = blocks.nlog10_ff(10, 1, 0)
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(10, 1, 0)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(2)
        self.blocks_moving_average_xx_0_0 = blocks.moving_average_ff(intSize, (1/intSize), intSize, 1)
        self.blocks_moving_average_xx_0 = blocks.moving_average_ff(intSize, (1/intSize), intSize, 1)
        self.blocks_complex_to_mag_squared_0_0 = blocks.complex_to_mag_squared(1)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)
        self.band_pass_filter_0 = filter.fir_filter_ccc(
            1,
            firdes.complex_band_pass(
                1,
                2e6,
                (-1000e3),
                (-450e3),
                20e3,
                window.WIN_BLACKMAN,
                6.76))


        ##################################################
        # Connections
        ##################################################
        self.connect((self.band_pass_filter_0, 0), (self.blocks_complex_to_mag_squared_0_0, 0))
        self.connect((self.band_pass_filter_0, 0), (self.qtgui_freq_sink_x_0_0, 2))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_moving_average_xx_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0_0, 0), (self.blocks_moving_average_xx_0_0, 0))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.blocks_nlog10_ff_0, 0))
        self.connect((self.blocks_moving_average_xx_0_0, 0), (self.blocks_nlog10_ff_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.probeSignalPower, 0))
        self.connect((self.blocks_nlog10_ff_0_0, 0), (self.probeSignalPowerNoise, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.digital_ofdm_tx_0_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.band_pass_filter_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.filter_fft_low_pass_filter_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.qtgui_freq_sink_x_0_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.digital_ofdm_tx_0_0, 0), (self.channels_channel_model_0, 0))
        self.connect((self.filter_fft_low_pass_filter_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.filter_fft_low_pass_filter_0, 0), (self.qtgui_freq_sink_x_0_0, 1))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "OFDM_Signal_Analyzer")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_variable_function_probe_signal(self):
        return self.variable_function_probe_signal

    def set_variable_function_probe_signal(self, variable_function_probe_signal):
        self.variable_function_probe_signal = variable_function_probe_signal
        self.set_signalPowerLabel(self.variable_function_probe_signal)
        self.set_snr((self.variable_function_probe_signal-self.variable_function_probe_noise))

    def get_variable_function_probe_noise(self):
        return self.variable_function_probe_noise

    def set_variable_function_probe_noise(self, variable_function_probe_noise):
        self.variable_function_probe_noise = variable_function_probe_noise
        self.set_noisePowerLabel(self.variable_function_probe_noise)
        self.set_snr((self.variable_function_probe_signal-self.variable_function_probe_noise))

    def get_snr(self):
        return self.snr

    def set_snr(self, snr):
        self.snr = snr
        Qt.QMetaObject.invokeMethod(self._snr_label, "setText", Qt.Q_ARG("QString", str(self._snr_formatter(self.snr))))

    def get_signalPowerLabel(self):
        return self.signalPowerLabel

    def set_signalPowerLabel(self, signalPowerLabel):
        self.signalPowerLabel = signalPowerLabel
        Qt.QMetaObject.invokeMethod(self._signalPowerLabel_label, "setText", Qt.Q_ARG("QString", str(self._signalPowerLabel_formatter(self.signalPowerLabel))))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.qtgui_freq_sink_x_0_0.set_frequency_range(self.cf, self.samp_rate)

    def get_packet_len(self):
        return self.packet_len

    def set_packet_len(self, packet_len):
        self.packet_len = packet_len
        self.blocks_stream_to_tagged_stream_0.set_packet_len(self.packet_len)
        self.blocks_stream_to_tagged_stream_0.set_packet_len_pmt(self.packet_len)
        self.blocks_vector_source_x_0.set_data(range(self.packet_len), ())

    def get_noise_voltage(self):
        return self.noise_voltage

    def set_noise_voltage(self, noise_voltage):
        self.noise_voltage = noise_voltage
        self.channels_channel_model_0.set_noise_voltage(self.noise_voltage)

    def get_noisePowerLabel(self):
        return self.noisePowerLabel

    def set_noisePowerLabel(self, noisePowerLabel):
        self.noisePowerLabel = noisePowerLabel
        Qt.QMetaObject.invokeMethod(self._noisePowerLabel_label, "setText", Qt.Q_ARG("QString", str(self._noisePowerLabel_formatter(self.noisePowerLabel))))

    def get_len_tag_key(self):
        return self.len_tag_key

    def set_len_tag_key(self, len_tag_key):
        self.len_tag_key = len_tag_key

    def get_intSize(self):
        return self.intSize

    def set_intSize(self, intSize):
        self.intSize = intSize
        self.blocks_moving_average_xx_0.set_length_and_scale(self.intSize, (1/self.intSize))
        self.blocks_moving_average_xx_0_0.set_length_and_scale(self.intSize, (1/self.intSize))

    def get_freq_offset(self):
        return self.freq_offset

    def set_freq_offset(self, freq_offset):
        self.freq_offset = freq_offset
        self.channels_channel_model_0.set_frequency_offset((self.freq_offset * 1.0/self.fft_len))

    def get_fft_len(self):
        return self.fft_len

    def set_fft_len(self, fft_len):
        self.fft_len = fft_len
        self.channels_channel_model_0.set_frequency_offset((self.freq_offset * 1.0/self.fft_len))

    def get_cf(self):
        return self.cf

    def set_cf(self, cf):
        self.cf = cf
        self.qtgui_freq_sink_x_0_0.set_frequency_range(self.cf, self.samp_rate)




def main(top_block_cls=OFDM_Signal_Analyzer, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
