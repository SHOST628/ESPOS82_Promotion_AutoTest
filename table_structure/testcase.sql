-- Create table
-- promid,amount 字段可去掉
create table TESTCASE
(
  serialno      INTEGER not null,
  testcaseid    VARCHAR2(100) not null,
  testcasedesci VARCHAR2(3000),
  itemcode      VARCHAR2(50),
  qty           NUMBER(15,4),
  originalprice      NUMBER(15,4),
  currsellingprice  NUMBER(15,4),
  unitprice     NUMBER(15,4),
  vipinfo           VARCHAR2(300),
  promlesstotal   NUMBER(15,4),
  promlessdetail      VARCHAR2(500),
  promparam_xg            VARCHAR2(1000),
  promparam_xc            VARCHAR2(1000),
  promparam_xp            VARCHAR2(1000),
  promparam_nc            VARCHAR2(1000),
  promparam_kdkp          VARCHAR2(1000),
  promparam_gt            VARCHAR2(1000),
  promparam_dis           VARCHAR2(1000),
  promparam_xe            VARCHAR2(1000),
  promparam_br            VARCHAR2(1000),
  promparam_bl            VARCHAR2(1000),
  testby        VARCHAR2(100),
  testtime      DATE,
  remarks       VARCHAR2(3000),
  promid        VARCHAR2(1000),
  promparameter VARCHAR2(3000),
  amount        NUMBER(15,4)
)
tablespace DATA01
  pctfree 10
  initrans 1
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );
-- Create/Recreate indexes
create index TESTCASE_D1 on TESTCASE (SERIALNO, TESTCASEID)
  tablespace DATA01
  pctfree 10
  initrans 2
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );

