#include <Python.h>

/*
 * class Scene:
 *     def __new__(cls, *a, **kw):
 *         scene_obj = object.__new__(cls)
 *         scene_obj._scene = ""
 *         return scene_obj
 *
 *     def __init__(self, scene=None):
 *         if scene and isinstance(scene, 'str'):
 *             self._scene = scene
 *
 *     @property
 *     def scene(self):
 *         return self._scene
 *
 *     @scene.setter
 *     def scene(self, value):
 *         if not value or not isinstance(value, str):
 *             raise TypeError("value should be unicode")
 *         self._scene = value
 */

typedef struct {
    PyObject_HEAD
    PyObject *scene;
} SceneObject;

static void
Scene_dealloc(SceneObject *self)
{
    Py_XDECREF(self->scene);
    Py_TYPE(self)->tp_free((PyObject *) self);
}

static PyObject *
Scene_new(PyTypeObject *type, PyObject *args, PyObject *kw)
{
    int rc = -1;
    SceneObject *self = NULL;
    self = (SceneObject *) type->tp_alloc(type, 0);

    if (!self) goto error;

    /* allocate attributes */
    self->scene = PyUnicode_FromString("");
    if (self->scene == NULL) goto error;

    rc = 0;
error:
    if (rc < 0) {
        Py_XDECREF(self->scene);
        Py_XDECREF(self);
    }
    return (PyObject *) self;
}

static int
Scene_init(SceneObject *self, PyObject *args, PyObject *kw)
{
    int rc = -1;
    static char *keywords[] = {"scene", NULL};
    PyObject *scene = NULL, *ptr = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, kw,
                                    "|O", keywords,
                                    &scene))
    {
        goto error;
    }

    if (scene && PyUnicode_Check(scene)) {
        ptr = self->scene;
        Py_INCREF(scene);
        self->scene = scene;
        Py_XDECREF(ptr);
    }

    rc = 0;
error:
    return rc;
}

static PyObject *
Scene_getscene(SceneObject *self, void *closure)
{
    Py_INCREF(self->scene);
    return self->scene;
}

static int
Scene_setscene(SceneObject *self, PyObject *value, void *closure)
{
    int rc = -1;

    if (!value || !PyUnicode_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "value should be unicode");
        goto error;
    }
    Py_INCREF(value);
    Py_XDECREF(self->scene);
    self->scene = value;
    rc = 0;
error:
    return rc;
}

static PyGetSetDef Scene_getsetters[] = {
    {"scene", (getter)Scene_getscene, (setter)Scene_setscene}
};

static PyTypeObject SceneType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "scene.Scene",             /* tp_name */
    sizeof(SceneObject),       /* tp_basicsize */
    0,                         /* tp_itemsize */
    (destructor) Scene_dealloc,/* tp_dealloc */
    0,                         /* tp_print */
    0,                         /* tp_getattr */
    0,                         /* tp_setattr */
    0,                         /* tp_reserved */
    0,                         /* tp_repr */
    0,                         /* tp_as_number */
    0,                         /* tp_as_sequence */
    0,                         /* tp_as_mapping */
    0,                         /* tp_hash  */
    0,                         /* tp_call */
    0,                         /* tp_str */
    0,                         /* tp_getattro */
    0,                         /* tp_setattro */
    0,                         /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT |
        Py_TPFLAGS_BASETYPE,   /* tp_flags */
    "Scene objects",           /* tp_doc */
    0,                         /* tp_traverse */
    0,                         /* tp_clear */
    0,                         /* tp_richcompare */
    0,                         /* tp_weaklistoffset */
    0,                         /* tp_iter */
    0,                         /* tp_iternext */
    0,                         /* tp_methods */
    0,                         /* tp_members */
    Scene_getsetters,          /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    (initproc) Scene_init,     /* tp_init */
    0,                         /* tp_alloc */
    Scene_new,             /* tp_new */
};


static PyModuleDef module = {
    PyModuleDef_HEAD_INIT, "scene", NULL, -1, NULL
};

PyMODINIT_FUNC
PyInit_scene(void)
{
    PyObject *m = NULL;
    if (PyType_Ready(&SceneType) < 0)
        return NULL;
    if ((m = PyModule_Create(&module)) == NULL)
        return NULL;
    Py_XINCREF(&SceneType);
    PyModule_AddObject(m, "Scene", (PyObject *) &SceneType);
    return m;
}