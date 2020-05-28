#import scene
#o=scene.Scene()
#print("ll")


M=True
if M :
    import sysconfig
    from distutils.core import setup, Extension

    cflags = sysconfig.get_config_var("CFLAGS")

    extra_compile_args = ["/std:c++latest"] if cflags is None else (cflags.split()+["-Wextra"])


    ext = Extension(
        "scene", ["scene.cpp"],
        extra_compile_args=extra_compile_args
    )

    setup(name="scene", version="1.0", ext_modules=[ext])
