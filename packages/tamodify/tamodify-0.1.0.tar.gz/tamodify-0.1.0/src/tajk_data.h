#ifndef	tajk_data_h
#define tajk_data_h

#ifdef __cplusplus
extern "C"  {
#endif

struct stru_tajk_field	{	//字段数据字典表
	int ver;	//版本，目前支持2.1和2.2，对应取值为21和22，为0表示数组结束
	int id;		//字段原始id
	char name[50],type;		//字段名，类型（C、A、N）
	int size,decpos;		//大小，小数位置
	char desc[1500];			//描述
};

struct stru_tajk_datafile_field{//各接口文件字段列表
	int ver;	//版本，目前支持2.1和2.2，对应取值为21和22，为0表示数组结束
	char filemode[3];//文件类型,如01,02这样
	int tfid;	//字段id，注意这里的id不是接口里的原始id，而是tajk_field中对应的序号
};

extern struct stru_tajk_field tajk_field[];	//全部字段数据字典表
extern struct stru_tajk_datafile_field tajk_datafile_field[];//数据文件和字段对应关系

#ifdef __cplusplus
}
#endif

#endif
