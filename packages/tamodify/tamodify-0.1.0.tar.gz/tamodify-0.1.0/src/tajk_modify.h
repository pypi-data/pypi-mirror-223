#ifndef TAJK_LIB_H
#define TAJK_LIB_H
#include <stdio.h>
#include <stdarg.h>
#include <stdlib.h>
#include "tajk_data.h"

#ifdef __cplusplus
extern "C"  {
#endif

/*
�޸�TA�ӿ��ļ��Ŀ⡣δ�����̰߳�ȫ

����ԭ�ļ���ֱ�Ӹ�д��ֻ�ṩ���������еĸ�д������һ���ļ����и��ƣ��ڸ��ƵĹ����п��Ը�д���ݣ�Ҳ���Ժ���ĳ�в���д��
���޸��ļ����ݣ����޸��ļ�ͷ

��������������£�

stru_ta_modify tm;  //����һ���ṹ
tamodify_init(&tm);  //��ʼ�����л�������ṹ�������������Ҫ��ͬһ��������ͬʱʹ�ö���ṹ����Ҫ��tm.use()�л���
tm.open(Դ�ļ���Ŀ���ļ���   �������ļ���Դ�ļ�ֻ����Ŀ���ļ�ֻд����ʱ�Ѿ������ļ�ͷ���
while(tm.read()){//����һ��
    tm.get(����,&���������;//��Դ�ļ��л�ȡ��������
    tm.get(����,�ַ�������);//��Դ�ļ��л�ȡ����
    tm.setd(����,���������;//���ø���������д��Ŀ���ļ�
    tm.set(����,�ַ�������);//����������д��Ŀ���ļ�
    tm.write();//�ѵ�ǰ�޸Ĺ�����д��Ŀ���ļ������û����һ�䣬����Ŀ���ļ��к�����һ��
};
if(tm.errno)˵���ոյĹ��̳����˴�����Ҫ�����������
tm.close();//д���ļ�β�������������ر������ļ�

*/
extern int tajk_retcode;//��¼����ķ�����
extern char tajk_retmsg[1000];//��¼����ķ�����Ϣ

typedef struct {
    int errnum;//����Ĵ�����
    char errinfo[1000];//����Ĵ�����Ϣ
    
    int (*open)(const char * fnsrc,const char * fndst);//��2���ļ���ʼ���ơ��޸�
    int (*read)();//��һ������
    int (*write)();//���޸Ĺ�������д��
    int (*close)();//��β�����ر��ļ�������д�����ֱ�ӹر��ļ������ܲ����Ƿ����������Ӧ�õ����������
    int (*get)(const char * colname,void * val);//�����ֶ�����ȡ�ַ���
    int (*setd)(const char * colname,double val);//�����ֶ������ø�������
    int (*sets)(const char * colname,const char * val);//�����ֶ��������ַ���
    int (*empty)(int arg);//0��������ֶΣ�1������У���ֵ����Ϊ0
    
    void (*perrinfo)(int retcode,const wchar_t *errinfo);//�û����Զ���һ�����������Ϣ�ĺ�������������ʹ��һ���պ���
    
    int ver;    //�汾�ţ�2.1�汾����21,2.2�汾����22������ֵ��ʾ����
    int isidx;//д���ļ�βʱ�����ļ��Ĵ���������ļ���Щ���죬������Ҫ������д�������ļ�����д�������ļ�����Ӧ�ò���Ҫ��
    char mode[8];//ģʽ���������ļ��е�OFI�������ļ��е�01,03
    char sender[30],recver[30];//�����ߣ�������
    char workday[10];//8λ��������

    struct stru_fielddata   {
        char name[50],type;
        int size,pos;//��С,Ϊ0��ʾ�ṹ�������;������λ��
        double rratio,wratio;//���ڴ������ݵ�С������,�ֱ����ڶ���д
    }sd[1000];//�ֶα�
    int fieldnum;//sd�Ĵ�С
    int recordcount,totalcount;//����ļ�¼�����ܼ�¼��
    int linesize;//�����ļ�ͷ����õ����г���
    char linedata[10000];//�����ݣ����ڶ���д������
    char fname[100];//������Ŀ¼��Ϣ�Ĵ򿪵��ļ�����Ϣ
    FILE *fjk,*fr,*fw;
    long totalcountpos;//��¼totalcount��λ�ã����ڽ�����ʱ���д�����ļ�¼��
    int totalcountwidth;//��¼totalcount�Ŀ�ȣ����ڻ�дʱ���ƿ��
    int writecount;//д�����    
    
    int stdlinesize;//������
    int totalrecord;
    int totalrecordpos;
}stru_ta_modify;

stru_ta_modify * tamodify_init(stru_ta_modify *);//��ʼ�����л�һ��ʵ��,�ÿ�ָ��������һ���ṹ
int tamodify_use(stru_ta_modify *);//�л�һ��ʵ��

int tamodify_open(const char * fnsrc,const char * fndst);//��2���ļ���ʼ���ơ��޸�,��Ӧ���ṹ���open
int tamodify_read();//����һ�����ݣ���Ӧ���ṹ���read
int tamodify_write();//дһ�����ݣ���Ӧ���ṹ���write
int tamodify_close();//���ر��ļ��ȴ�����Ӧ���ṹ���close
int tamodify_get(const char * colname,void * val);//�����ֶ�����ȡ����
int tamodify_setd(const char * colname,double val);//�����ֶ������ø�������
int tamodify_sets(const char * colname,const char * val);//�����ֶ��������ַ���
int tamodify_empty(int arg);//0��������ֶΣ�1������У���ֵ����Ϊ0

#ifdef __cplusplus
}
#endif

#endif
