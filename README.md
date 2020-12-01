# scikinC
Set of tools to translate scikit learn and keras neural network in plain C. 

[![Write in C parody](https://img.youtube.com/vi/1S1fISh/0.jpg)](https://www.youtube.com/watch?v=1S1fISh)


## CLI

Create the C file with the exported model
```
python3 -m scikinC some_model.pkl > Cfile.C
```

Compile the C file for dynamic loading 
```
gcc -o Cfile.so Cfile.C -shared -fPIC -Ofast
```

Use it everywhere
```
#include  <dlfcn.h>

typedef float *(*mlfunc)(float *, const float*);

void somewhere_in_your_code (void)
{
  void *handle = dlopen ( "./Cfile.so", RTLD_LAZY );
  if (!handle)
    std::cout << "dlerror: " << dlerror() << std::endl; 

  mlfunc minmax = mlfunc(dlsym (handle, "a_minmaxscaler")); 
  float *inp [] = { /* your input goes here */ };
  float *out [ /*output n_features goes here*/ ];
  minmax ( out, inp ); 

  dlclose(handle); 
}
```

## Implemented converters

scikit-learn:
 * GradientBoostingClassifier (binary classification and multiclass)
 * MinMaxScaler 

keras:
 * Sequential model
 * Dense layer 
 * tanh activation function
 * relu activation function 
 * sigmoid activation function 

