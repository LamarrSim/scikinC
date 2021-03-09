import numpy as np
from scikinC import BaseConverter
from scipy import stats
from ._tools import get_n_features 

from scikinC import convert 


class PipelineConverter (BaseConverter):
  def __init__(self):
    pass

  def convert(self, model, name=None):
    lines = [] 

    def prefixed (stepname):
      return stepname if name is None else "%s_%s" % (name, stepname)

    for sname, step in model.steps: 
      lines.append ( convert ({prefixed(sname):step}) ) 
    


    lines += self.header()

    lines.append("""
    extern "C"
    float *%(name)s (float* ret, const float *x)
    {
    """ % (dict(name=name)))

    input_name = 'x' 
    for sname, step in model.steps[:-1]:
      lines.append ( """
      float out_%(name)s[%(nFeatures)d];
      %(name)s ( out_%(name)s, %(input_name)s  );
      """ % dict (
        name = prefixed(sname),
        nFeatures = get_n_features ( step ), 
        input_name = input_name ,
        ))
      input_name = "out_%s" % prefixed(sname) 

    sname, step = model.steps[-1] 
    lines.append ( """
      %(name)s ( ret, %(input_name)s  );
    """ % dict (
      name = prefixed(sname),
      input_name = input_name ,
      ))
      

    lines.append("""
      return ret;
    }
    """)


    lines.append("""
    extern "C"
    float *%(name)s_inverse (float* ret, const float *x)
    {
    """ % (dict(name=name)))

    input_name = 'x' 
    for sname, step in model.steps[::-1][:-1]:
      lines.append ( """
      float out_%(name)s[%(nFeatures)d];
      %(name)s_inverse ( out_%(name)s, %(input_name)s  );
      """ % dict (
        name = prefixed(sname),
        nFeatures = get_n_features ( step ), 
        input_name = input_name ,
        ))
      input_name = "out_%s" % prefixed(sname) 

    sname, step = model.steps[0] 
    lines.append ( """
      %(name)s_inverse ( ret, %(input_name)s  );
    """ % dict (
      name = prefixed(sname),
      input_name = input_name ,
      ))
      

    lines.append("""
      return ret;
    }
    """)

    return "\n".join(lines) 
