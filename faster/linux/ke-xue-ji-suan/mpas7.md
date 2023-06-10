# MPAS7

{% embed url="https://mpas-dev.github.io/" %}
MPAS Atmosphere home page
{% endembed %}

## 安装环境

从home page找到User's Guide，阅读文档，MPAS-A需要netcdf、parallel-netcdf、parallelio库

spack创建新环境`spack env create mpas7`，随后激活环境`spack env activate mpas7`

修改环境下的`spack.yaml`，添加以下包，然后`spack install`安装

```yaml
spack:
  specs:
  - netcdf-c @4.4.1.1
  - netcdf-fortran @4.4.4
  - parallel-netcdf @1.8.1
  - parallelio
  view: true
```

## 配置环境

新建libs文件夹，存放依赖库。写一个脚本link.sh，将包(库)从spack安装目录下导过来。

```sh
dirs=( "openmpi" "netcdf" "pio2" "all")
for d in ${dirs[@]}
do
    if [ ! -d $d ]
    then
        mkdir $d
        echo "non dir named $d and then mkdir $d"
    else
        echo "found dir $d"
    fi
done

type_of_compiler=gcc #[gcc, intel]
path_of_spack=$(ls -d /home/$USER/Software/spack/opt/spack/$(spack arch)/$type_of_compiler*)
if [[ -e $path_of_spack ]]
then
    echo "found $path_of_spack"
else
    echo "No such file or dir:$path_of_spack"
    exit 1
fi

path_of_openmpi=$(ls -d $path_of_spack/openmpi*/)
path_of_netcdf_c=$(ls -d $path_of_spack/netcdf-c*)
path_of_netcdf_f=$(ls -d $path_of_spack/netcdf-f*)
path_of_netcdf_para=$(ls -d $path_of_spack/parallel-netcdf*)
path_of_pio2=$(ls -d $path_of_spack/parallelio*)

# dirs=( $path_of_mpich $path_of_hdf5 $path_of_zlib $path_of_netcdf_c $path_of_netcdf_f )
dirs=( $path_of_openmpi $path_of_netcdf_c $path_of_netcdf_f $path_of_netcdf_para $path_of_pio2 )
for d in ${dirs[@]}
do
    if [[ -e $d ]]
    then
        echo "found $d"
    else
        echo "No such file or dir:$d"
        exit 1
    fi
done

rm -rf openmpi/*
cp -r $path_of_openmpi/* openmpi/

rm -rf netcdf/*
cp -r $path_of_netcdf_c/* netcdf/
cp -r $path_of_netcdf_f/* netcdf/
cp -r $path_of_netcdf_para/* netcdf/

rm -rf pio2/*
cp -r $path_of_pio2/* pio2/

rm -rf all/*
cp -r openmpi/* all/
cp -r netcdf/* all/
cp -r pio2/* all/
```

再写一个脚本setenv.sh，用来设置环境变量

```sh
DIR=/home/$USER/MPAS7/libs
export NETCDF=$DIR/netcdf
export PNETCDF=$DIR/netcdf
export PIO=$DIR/pio2

export CORE=atmosphere
export USE_PIO2=true
```

## 编译

根据文档描述，使用pio2时建议在cmake时设置`-DPIO ENABLE TIMING=OFF`，打开makefile文件，找到将要使用的编译器对应一块，添加这个编译选项到CPPFLASGS。

`source ../libs/setenv.sh`加载环境变量，`make gfortran`开始编译
