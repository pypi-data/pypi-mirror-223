#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "tajk_modify.h"

static stru_ta_modify tm;

static char * srtrim(char *s){//清除字符串尾部的空白
    int i=strlen(s)-1;
    for(;i>=0;i--){
        if(isspace(s[i]))s[i]=0;
        else break;
    };
    return s;
}

static PyObject *
p_open(PyObject *self, PyObject *args)
{
    PyObject * field;
    char *fnsrc,*fndst;//源文件名，目标文件名
    int jg,i;
    if (!PyArg_ParseTuple(args, "ss", &fnsrc,&fndst))return NULL;
    jg=tamodify_open(fnsrc,fndst);
    if(jg==0){
        field=PyList_New(0);
        for(i=0;i<tm.fieldnum;i++){
            PyList_Append(field,Py_BuildValue("s", tm.sd[i].name));
        };
        PyModule_AddObject(self,"field",field);
    };
    return PyLong_FromLong(jg);
}

static PyObject *
p_close()
{
    return PyLong_FromLong(tamodify_close());
}

static PyObject *
p_read()
{
    return PyLong_FromLong(tamodify_read());
}

static PyObject *
p_write()
{
    return PyLong_FromLong(tamodify_write());
}

static PyObject *
p_get(PyObject *self, PyObject *args)
{
    char data[3000];
    int i;
    char * colname;//字段名
    double dval;//数值型数据
    if (!PyArg_ParseTuple(args, "s", &colname))return NULL;
    for(i=0;i<tm.fieldnum;i++){
        if(strcasecmp(colname,tm.sd[i].name)!=0)continue;
        memcpy(data,tm.linedata+tm.sd[i].pos,tm.sd[i].size);//读入字段
        data[tm.sd[i].size]=0;//结尾清0
        srtrim(data);//清除结尾的空白
        if(tm.sd[i].type=='C' || tm.sd[i].type=='A'){//字符型
            return Py_BuildValue("s",data);
        }else{
            if(sscanf(data,"%lf",&dval)==1){//正常读入数据
                dval=dval * tm.sd[i].rratio;
                return Py_BuildValue("f",dval);
            }else{
                return Py_BuildValue("f",0);
            };
        };
        return NULL;//类型不对
    };
    return NULL;//字段名没找到
}

static PyObject *
p_set(PyObject *self, PyObject *args)
{
    char * data;
    char * colname;//字段名
    double dval;//数值型数据
    if(PyNumber_Check(args)){//如果参数是数值
        if (!PyArg_ParseTuple(args, "sd", &colname,&dval))return NULL;
        return PyLong_FromLong(tamodify_setd(colname,dval));
    }else{
        if (!PyArg_ParseTuple(args, "ss", &colname,&data))return NULL;
        return PyLong_FromLong(tamodify_sets(colname,data));
    };
}

static PyMethodDef pMethods[] = {
    {"open",  p_open, METH_VARARGS,"open(源文件名,目标文件名)\n指定源文件、目标文件开始复制、修改"},
    {"close",  p_close, METH_VARARGS,"close()\n最后一步操作：写文件尾，重置记录数量，关闭打开的文件"},
    {"read",  p_read, METH_VARARGS,"read()\n读入源文件中一行数据到缓冲区"},
    {"write",  p_write, METH_VARARGS,"read()\n把缓冲区中数据写入目标文件中"},
    {"get",  p_get, METH_VARARGS,"get(字段名)\n读取缓冲区中字段的值，根据字段类型返回字符串或者是数值"},
    {"set",  p_set, METH_VARARGS,"set(字段名,数据)\n更新缓冲区中字段的值"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef pmodule = {
    PyModuleDef_HEAD_INIT,
    "tamodify",   /* name of module */
    NULL, /* module documentation, may be NULL */
    -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
    pMethods
};

PyObject *
PyInit_tamodify(void){
    PyObject * m;
    tamodify_init(&tm);
    m=PyModule_Create(&pmodule);
    return m;
}
