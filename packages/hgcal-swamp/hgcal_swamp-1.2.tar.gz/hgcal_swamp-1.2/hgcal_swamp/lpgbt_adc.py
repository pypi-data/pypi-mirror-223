import logging
import util
from typing import Union, TypeVar, Dict, Any

T = TypeVar('T', bound='lpgbt_adc_channel')

class lpgbt_adc_channel:
    def __init__(self, cfg: Dict[str, Any]):
        '''
        lpGBT ADC channel class

        Arguments:
            cfg: configuration dictionary
                {name: name of the ADC channel,
                lpgbt: lpGBT object,
                channel_p: positive channel,
                channel_n: negative channel}
        '''
        try:
            self.logger = logging.getLogger( 'lpbgt_adc' )
            self.name = cfg['name']
            self.lpgbt = cfg['lpgbt']
            self.channel_p = cfg['channel_p']
            self.channel_n = cfg['channel_n']
            self.logger = logging.getLogger( f'lpgbt_adc_channel.{self.name}' )
            self.logger.info(f'creating an instance of lpgbt_adc_channel.{self.name}')
        except:
            self.logger.critical(f'Wrong configuration format when creating {self.logger.name}')
            self.logger.critical(f'Configuration used : {cfg}')
            self.logger.critical(f'exit')
            exit(1)

    def __str__(self) -> str:
        return f'lpgbt_adc_channel; Name : {self.name}, channel_p: {self.channel_p}, channel_n: {self.channel_n}'
    
    def __eq__(self,other: T) -> bool:
        return self.name==other.name and self.channel_p==other.channel_p and self.channel_n==other.channel_n
    
    def setLoggingLevel(self,level):
        util.setLoggingLevel(level,self.logger)
    
    def read(self, n_samples: int = 1, gain: int = 0) -> Union[int, list]:
        '''
        Reads the ADC channel

        Arguments:
            n_samples: number of samples to return
            gain: gain of the ADC (0 = 1, 1 = 32)

        Returns:
            Raw ADC reading
        '''
        self.lpgbt.adc_config(self.channel_p, self.channel_n, gain)
        return self.lpgbt.adc_convert(n_samples)

    def read_voltage(self, n_samples: int = 1, gain: int = 0) -> Union[float, list]:
        '''
        Reads the ADC channel and returns the voltage

        Arguments:
            n_samples: number of samples to return
            gain: gain of the ADC (0 = 1, 1 = 32)

        Returns:
            ADC reading in volts
        '''
        reading = self.read(n_samples, gain)
        if isinstance(reading, list):
            return [r/(self.lpgbt.ADC_MAX * self.lpgbt.VREF_NOMINAL) for r in reading]
        else:
            return reading/(self.lpgbt.ADC_MAX * self.lpgbt.VREF_NOMINAL)
    
    def current_dac_setup(self, code: int, enable: bool = True) -> None:
        '''
        Sets up the DAQ

        Arguments:
            code: current DAC output code
            enable: current DAQ enable
        '''
        if self.channel_p > self.lpgbt.AdcInputSelect.EXT7:
            self.logger.error(f'Channel {self.channel_p} is not supported for DAQ')
            return
        
        if code > 255 or code < 0:
            self.logger.error(f'Current code {code} is invalid')
            return
        
        current_chn_enable = self.lpgbt.read_reg(self.lpgbt.CURDACCHN)
        
        
        if enable:
            current_chn_enable |= 1 << self.channel_p
        else:
            current_chn_enable &= ~(1 << self.channel_p)
        
        config = self.lpgbt.read_reg(self.lpgbt.DACCONFIGH)
        if current_chn_enable:
            config |= self.lpgbt.DACCONFIGH.CURDACENABLE.bit_mask
        else:
            config &= ~self.lpgbt.DACCONFIGH.CURDACENABLE.bit_mask
        
        self.lpgbt.write_reg(self.lpgbt.CURDACCHN, current_chn_enable)
        self.lpgbt.write_reg(self.lpgbt.DACCONFIGH, config)
        self.lpgbt.write_reg(self.lpgbt.CURDACVALUE, code)

    def set_channels(self, channel_p: int, channel_n: int) -> None:
        '''
        Sets the ADC channels

        Arguments:
            channel_p: positive channel
            channel_n: negative channel
        '''
        self.set_channel_p(channel_p)
        self.set_channel_n(channel_n)

    def set_channel_p(self, channel_p: int) -> None:
        '''
        Sets the ADC positive channel

        Arguments:
            channel_p: positive channel
        '''
        self.channel_p = channel_p

    def set_channel_n(self, channel_n: int) -> None:
        '''
        Sets the ADC negative channel

        Arguments:
            channel_n: negative channel
        '''
        self.channel_n = channel_n