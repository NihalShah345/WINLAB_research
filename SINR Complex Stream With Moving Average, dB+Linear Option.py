import numpy as np
from gnuradio import gr


class blk(gr.sync_block):

    def __init__(self, window=16, scaleType='dB'):  
        gr.sync_block.__init__(
            self,
            name='SINR Complex Input Streams w/ Moving Average, Decibel/Linear Scale',  
            in_sig=[np.complex64, np.complex64],
            out_sig=[np.float32] 
        )
        
        self.window = int(window)
        self.scaleType = scaleType  # preserve original casing
        self.calibration = np.ones(self.window) / self.window

    def work(self, input_items, output_items):
        signalNoise = input_items[0]
        noise = input_items[1]
        finalSINR = output_items[0]

        minLength = min(len(signalNoise), len(noise))
        if minLength < self.window:
            return 0

        powerSignalNoise = np.abs(signalNoise[:minLength])**2
        powerNoise = np.abs(noise[:minLength])**2 + 1e-12

        smoothPowerSignalNoise = np.convolve(powerSignalNoise, self.calibration, mode='valid')
        smoothPowerNoise = np.convolve(powerNoise, self.calibration, mode='valid')
        SINRratio = smoothPowerSignalNoise / (1e-12 + smoothPowerNoise)

        # Case-insensitive comparison
        if self.scaleType.lower() == 'db':
            SINR = 10 * np.log10(SINRratio)
        elif self.scaleType.lower() == 'linear':
            SINR = SINRratio
        else:
            raise ValueError("Invalid scaleType. Use 'dB' or 'linear'.")

        numberSamples = min(len(SINR), len(finalSINR))
        finalSINR[:numberSamples] = SINR[:numberSamples]

        return numberSamples
