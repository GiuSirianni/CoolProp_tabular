from __future__ import division, print_function
import numpy as np
from CPIncomp.BaseObjects import IncompressibleData

class SolutionDataWriter(object):
    """ 
    A base class that defines all the variables needed 
    in order to make a proper fit. You can copy this code
    put in your data and add some documentation for where the
    information came from. 
    """
    def __init__(self):
        self.verbose = True
    
    def fitAll(self, data):
        T = data.temperature.data
        x = data.concentration.data
        
        #if data.Tbase==0.0:
        #    data.Tbase = (np.min(T) + np.max(T)) / 2.0
        #if data.xbase==0.0:
        #    data.xbase = (np.min(x) + np.max(x)) / 2.0
            
        # Set the standard order for polynomials
        std_xorder = 3
        std_yorder = 5
        std_coeffs = np.zeros((std_xorder,std_yorder))
        
        errList = (ValueError, AttributeError, TypeError, RuntimeError)
        
        try:
            data.density.coeffs = np.copy(std_coeffs)
            data.density.type   = data.density.INCOMPRESSIBLE_POLYNOMIAL
            data.density.fit(T,x,data.Tbase,data.xbase)
        except errList as ve:
            if self.verbose: print("Could not fit density coefficients:", ve)
            pass        

        try:        
            data.specific_heat.coeffs = np.copy(std_coeffs)
            data.specific_heat.type   = data.specific_heat.INCOMPRESSIBLE_POLYNOMIAL
            data.specific_heat.fit(T,x,data.Tbase,data.xbase)
        except errList as ve:
            if self.verbose: print("Could not fit specific heat coefficients:", ve)
            pass
        
        try:
            data.viscosity.coeffs = np.copy(std_coeffs)
            data.viscosity.type   = data.viscosity.INCOMPRESSIBLE_EXPPOLYNOMIAL
            data.viscosity.fit(T,x,data.Tbase,data.xbase)
        except errList as ve:
            if self.verbose: print("Could not fit viscosity coefficients:", ve)
            pass

        try:        
            data.conductivity.coeffs = np.copy(std_coeffs)
            data.conductivity.type   = data.conductivity.INCOMPRESSIBLE_POLYNOMIAL
            data.conductivity.fit(T,x,data.Tbase,data.xbase)
        except errList as ve:
            if self.verbose: print("Could not fit conductivity coefficients:", ve)
            pass
        
        try:
            data.saturation_pressure.coeffs = np.copy(std_coeffs)
            data.saturation_pressure.type   = data.saturation_pressure.INCOMPRESSIBLE_EXPPOLYNOMIAL
            data.saturation_pressure.fit(T,x,data.Tbase,data.xbase)
        except errList as ve:
            if self.verbose: print("Could not fit saturation pressure coefficients:", ve)
            pass

        try:        
            data.T_freeze.coeffs = np.copy(std_coeffs)
            data.T_freeze.type   = data.T_freeze.INCOMPRESSIBLE_POLYNOMIAL
            data.T_freeze.fit(0.0,x,0.0,data.xbase)
        except errList as ve:
            if self.verbose: print("Could not fit TFreeze coefficients:", ve)
            pass

        try:        
            data.volume2mass.coeffs = np.copy(std_coeffs)
            data.volume2mass.type   = data.volume2mass.INCOMPRESSIBLE_POLYNOMIAL
            data.volume2mass.fit(T,x,data.Tbase,data.xbase)
        except errList as ve:
            if self.verbose: print("Could not fit V2M coefficients:", ve)
            pass

        try:        
            data.mass2mole.coeffs = np.copy(std_coeffs)
            data.mass2mole.type   = data.mass2mole.INCOMPRESSIBLE_POLYNOMIAL
            data.mass2mole.fit(T,x,data.Tbase,data.xbase)
        except errList as ve:
            if self.verbose: print("Could not fit M2M coefficients:", ve)
            pass
        
    
    def toJSON(self,data):
        jobj = {}
        
        jobj['name'] = data.name # Name of the current fluid
        jobj['description'] = data.description # Description of the current fluid
        jobj['reference'] = data.reference # Reference data for the current fluid
        
        jobj['Tmax'] = data.Tmax         # Maximum temperature in K
        jobj['Tmin'] = data.Tmin         # Minimum temperature in K
        jobj['xmax'] = data.xmax         # Maximum concentration
        jobj['xmin'] = data.xmin         # Minimum concentration
        jobj['TminPsat'] = data.TminPsat     # Minimum saturation temperature in K
        jobj['Tbase'] = data.Tbase       # Base value for temperature fits
        jobj['xbase'] = data.xbase       # Base value for concentration fits
    
        #data.temperature  # Temperature for data points in K
        #data.concentration  # Concentration data points in weight fraction
        jobj['density'] = data.density.toJSON() # Density in kg/m3
        jobj['specific_heat'] = data.specific_heat.toJSON() # Heat capacity in J/(kg.K)
        jobj['viscosity'] = data.viscosity.toJSON() # Dynamic viscosity in Pa.s
        jobj['conductivity'] = data.conductivity.toJSON() # Thermal conductivity in W/(m.K)
        jobj['saturation_pressure'] = data.saturation_pressure.toJSON() # Saturation pressure in Pa
        jobj['T_freeze'] = data.T_freeze.toJSON() # Freezing temperature in K
        jobj['volume2mass'] = data.volume2mass.toJSON() # dd
        jobj['mass2mole'] = data.mass2mole.toJSON() # dd
        
        import json
        
        
        original_float_repr = json.encoder.FLOAT_REPR 
        json.encoder.FLOAT_REPR = lambda o: format(o, ' .15e') 
        #print json.dumps(1.0001) 
        dump = json.dumps(jobj, indent = 2, sort_keys = True)
        json.encoder.FLOAT_REPR = original_float_repr
        
        #print dump
                
        fp = open(jobj['name']+'.json', 'w')
        fp.write(dump)
        fp.close()