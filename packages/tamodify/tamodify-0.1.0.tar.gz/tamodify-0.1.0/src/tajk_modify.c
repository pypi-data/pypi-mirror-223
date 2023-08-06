#include <ctype.h>
#include <string.h>
#include <sys/stat.h>
#include <locale.h>
#include "tajk_modify.h"

int tajk_retcode;//��¼����ķ�����
char tajk_retmsg[1000];//��¼����ķ�����Ϣ

static stru_ta_modify * tam;

static int rtn(int rtcode,const char *fmt,...){
   	char s[10000],savelocale[100];
	va_list ap;
	wchar_t ws[20000];
	if(rtcode==0){
	    return 0;
	};
	va_start(ap, fmt);
	vsnprintf(s,sizeof(s)-1,fmt,ap);
	va_end(ap);
	strcpy(savelocale,setlocale(LC_ALL,NULL));
	setlocale(LC_ALL, "zh_CN.utf8");
	mbstowcs(ws,s,sizeof(ws)/sizeof (wchar_t));
	setlocale(LC_ALL,"");
	tam->perrinfo(rtcode,ws);
	setlocale(LC_ALL,savelocale);
	return 0;
}

static char * srtrim(char *s){//����ַ���β���Ŀհ�
    int i=strlen(s)-1;
    for(;i>=0;i--){
        if(isspace(s[i]))s[i]=0;
        else break;
    };
    return s;
}

static int readline(){//��Դ�ļ�����һ�����ݵ�lindata
    if(tam->fr==NULL)return rtn(__LINE__,"�ļ�û�򿪲��ܶ�ȡ");
    if(fgets(tam->linedata,sizeof(tam->linedata),tam->fr)==NULL)return rtn(__LINE__,"���ļ�����");
    return 0;
}

static int readhead(char *t,int cd)   {//�ӻ����������ַ��������ĩβ�Ŀո�
    strcpy(t,"");
    if(readline())return 1;
    strncpy(t,tam->linedata,cd);
    t[cd-1]=0;
    srtrim(t);
    return tamodify_write();
}

static void default_perrinfo(int retcode,const wchar_t *errinfo){//�û����Զ���һ�����������Ϣ�ĺ�������������ʹ������պ���
}

int tamodify_open(const char * fnsrc,const char * fndst)    {//��2���ļ���ʼ���ơ��޸�
    char stemp[10000];
    int i;
    tam->errnum=0;
    strcpy(tam->errinfo,"");
    tam->totalcountpos=0;//����Ϊ0������д�ļ�ʱ���ۼ�writecountд�����
    tam->fr=fopen(fnsrc,"r");
    if(tam->fr==NULL)return rtn(-1,"��Դ�ļ�%s����",fnsrc);
    tam->fw=fopen(fndst,"w");
    if(tam->fw==NULL){
        return rtn(-1,"��Ŀ���ļ�%s����",fndst);
    };
    if(readhead(stemp,sizeof(stemp)))return __LINE__;
    if(strcmp(stemp,"OFDCFDAT")!=0)return rtn(__LINE__,"�����ļ�ͷӦ����OFDCFDAT");
    if(readhead(stemp,sizeof(stemp)))return __LINE__;
    sscanf(tam->linedata,"%d",&tam->ver);
    if(tam->ver!=22)tam->ver=21;//ʵ���з�����Щ�˻���ʹ��2.0�ӿڣ��͵�ͬ2.1�����
    if(readhead(tam->sender,sizeof(tam->sender)))return __LINE__;   //������
    if(readhead(tam->recver,sizeof(tam->recver)))return __LINE__;   //������
    if(readhead(tam->workday,sizeof(tam->workday)))return __LINE__; //����
    if(readhead(stemp,sizeof(stemp)))return __LINE__;       //����
    if(readhead(tam->mode,sizeof(tam->mode)))return __LINE__;       //�ļ����ͣ���01��02��07����
    if(readhead(stemp,sizeof(stemp)))return __LINE__;       //����
    if(readhead(stemp,sizeof(stemp)))return __LINE__;       //����
    if(readhead(stemp,sizeof(stemp)))return __LINE__;       //�ֶα�����
    sscanf(stemp,"%d",&tam->fieldnum);
    for(i=0,tam->linesize=0;i<tam->fieldnum;i++){
        if(readhead(stemp,sizeof(stemp)))return __LINE__;
        tam->sd[i].size=0;//���ж��Ƿ��������
        for(int j=0;tajk_field[j].ver;j++){
            if(tajk_field[j].ver!=tam->ver)continue;
            if(strcasecmp(tajk_field[j].name,stemp)!=0)continue;
            strcpy(tam->sd[i].name,tajk_field[j].name);
            tam->sd[i].type=tajk_field[j].type;
            tam->sd[i].size=tajk_field[j].size;
            tam->sd[i].rratio=tam->sd[i].wratio=1.0;
            for(int k=0;k<tajk_field[j].decpos;k++){
                tam->sd[i].rratio=tam->sd[i].rratio/10.0;
                tam->sd[i].wratio=tam->sd[i].wratio*10.0;
            };
            tam->sd[i].pos=tam->linesize;
            tam->linesize=tam->linesize+tam->sd[i].size;
            break;
        };
        if(tam->sd[i].size==0){//û���ҵ���Ӧ�ֶ�
            return rtn(__LINE__,"�ӿ��ֶα���û���ҵ��ֶ�%s",stemp);
        };
    };
    tam->totalcountpos=ftell(tam->fw);//��¼λ�ã����Ҫ������������д�˴�
    if(readhead(stemp,sizeof(stemp)))return __LINE__;
    if(sscanf(stemp,"%d",&tam->totalcount)!=1)return rtn(__LINE__,"�������ļ���������");
    tam->totalcountwidth=strlen(stemp);
    tam->recordcount=0;
    tam->writecount=0;
    return 0;
}

int tamodify_read() {//����һ�����ݣ���Ӧ���ṹ���read
    if(tam->recordcount==tam->totalcount)return 1;
    tam->recordcount++;
    return readline();
}

int tamodify_get(const char * colname,void * val){//�����ֶ�����ȡ����
    char data[3000];
    int i;
    for(i=0;i<tam->fieldnum;i++){
        if(strcasecmp(colname,tam->sd[i].name)!=0)continue;
        memcpy(data,tam->linedata+tam->sd[i].pos,tam->sd[i].size);//�����ֶ�
        data[tam->sd[i].size]=0;//��β��0
        srtrim(data);//�����β�Ŀհ�
        if(tam->sd[i].type=='C' || tam->sd[i].type=='A'){//�ַ���
            strcpy(val,data);
        }else{
            if(sscanf(data,"%lf",(double *)val)==1){//������������
                *(double *)val=*(double *)val * tam->sd[i].rratio;
            }else{
                return 1;
            };
        };
        return 0;
    };
    return rtn(__LINE__,"�ֶ���%s�ڽӿ��ļ���û�ҵ�",colname);
}

int tamodify_setd(const char * colname,double val){//�����ֶ������ø�������
    int i;
    char temp[1000];
    for(i=0;i<tam->fieldnum;i++){
        if(strcasecmp(colname,tam->sd[i].name)!=0)continue;
        sprintf(temp,"%0*.0lf",tam->sd[i].size,val * tam->sd[i].wratio);
        memcpy(tam->linedata+tam->sd[i].pos,temp,tam->sd[i].size);
        return 0;
    };
    return rtn(__LINE__,"�ֶ���%s�ڽӿ��ļ���û�ҵ�",colname);
}

int tamodify_sets(const char * colname,const char * val){//�����ֶ��������ַ���
    int i,k;
    for(i=0;i<tam->fieldnum;i++){
        if(strcasecmp(colname,tam->sd[i].name)!=0)continue;
        memset(tam->linedata+tam->sd[i].pos,' ',tam->sd[i].size);
        k=strlen(val);
        if(k>=tam->sd[i].size)k=tam->sd[i].size;
        memcpy(tam->linedata+tam->sd[i].pos,val,k);
        return 0;
    };
    return rtn(__LINE__,"�ֶ���%s�ڽӿ��ļ���û�ҵ�",colname);
}

int tamodify_empty(int arg)    {//0��������ֶΣ�1������У���ֵ����Ϊ0
    int i;
    for(i=0;i<tam->fieldnum;i++){
        
    };
    memset(tam->linedata,0,sizeof(tam->linedata));
    memset(tam->linedata,' ',tam->linesize);
    strcat(tam->linedata,"\r\n");
    return 0;
}

int tamodify_write()    {//����һ�����ݣ���Ӧ���ṹ���write
    if(tam->fw==NULL)return rtn(-1,"δ��д�ļ�");
    fprintf(tam->fw,"%s",tam->linedata);
    if(tam->totalcountpos>0)tam->writecount++;
    return 0;
}

int tamodify_close()    {//����һ�����ݣ���Ӧ���ṹ���close
    if(tam->errnum==0){//û�г��������������д���ļ�β
        fprintf(tam->fw,"OFDCFEND\r\n");
        fseek(tam->fw,tam->totalcountpos,SEEK_SET);
        fprintf(tam->fw,"%0*d\r\n",tam->totalcountwidth,tam->writecount);
    };
    if(tam->fr!=NULL){
        fclose(tam->fr);
        tam->fr=NULL;
    };
    if(tam->fw!=NULL){
        fclose(tam->fw);
        tam->fw=NULL;
    };
    return 0;
}

stru_ta_modify * tamodify_init(stru_ta_modify * ta_modify) {//��ʼ�����л�һ��ʵ��
    if(ta_modify==NULL){
        ta_modify=(stru_ta_modify *)malloc(sizeof(stru_ta_modify));
    };
    tam=ta_modify;
    tam->errnum=0;
    strcpy(tam->errinfo,"");
    tam->fr=NULL;
    tam->fw=NULL;
    tam->fieldnum=0;
    tam->open=tamodify_open;
    tam->read=tamodify_read;
    tam->write=tamodify_write;
    tam->close=tamodify_close;
    tam->perrinfo=default_perrinfo;
    tam->get=tamodify_get;
    tam->setd=tamodify_setd;
    tam->sets=tamodify_sets;
    tam->empty=tamodify_empty;
    return ta_modify;
}

static int setret(stru_ta_modify * tajk,int returncode,const char *fmt,...)  {//���÷����롢������Ϣ
    va_list ap;
    va_start(ap, fmt);
    vsnprintf(tajk_retmsg,sizeof(tajk_retmsg)-1,fmt,ap);
    va_end(ap);
    tajk_retcode=returncode;
    return returncode;
}

int tamodify_use(stru_ta_modify * ta_modify){//�л�һ��ʵ��
    tam=ta_modify;
    return 0;
}

int tajk_closeall(stru_ta_modify * tajk){//�رմ򿪵��ļ���
	if(tajk==NULL)return setret(tajk,-1,"����tajk_closeall�Ĳ���Ϊ��ֵ");
    if(tam->fjk!=NULL)fclose(tam->fjk);
    tam->fjk=NULL;
    return 0;
}

stru_ta_modify * tajk_init(){
	stru_ta_modify * tajk=(stru_ta_modify *)malloc(sizeof(stru_ta_modify));
	if(tajk==NULL)return NULL;
	tam->fjk=NULL;
	return tajk;
}
