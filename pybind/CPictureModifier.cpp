#include<pybind11/pybind11.h>
#include<pybind11/numpy.h>
#include<pybind11/stl.h>
#include<algorithm>
#include<iostream>
#include<string>
#include<stdio.h>
#include<math.h>
#include"gif.h"

#define PI 3.14159265359f

namespace py = pybind11;
using namespace std;

vector<int> clipVector(vector<int> _numbers, int lowerBound, int upperBound) {
    vector<int> numbers{_numbers};
	for (int i=0;i<_numbers.size();i++) {
        numbers[i] = max(lowerBound, min(upperBound, _numbers[i]));
    }
	return numbers;
}

template <typename T>//渡された範囲の画像(正方形のみ)の中心を画像サイズの小さい値をmrにしてゆらす0(入力、出力はmr*2とmr*2の正方形)
auto SquareCenterShake(py::array_t<T> image, int maxframe, int nowframe, vector<int> _ml) {
    const auto &buff_info = image.request();
    const auto &shape = buff_info.shape;
    py::array_t<T> result{shape};
    int sx=(int)shape[1];
    int sy=(int)shape[0];
    int mr=0;
    if(sy>sx){
        mr=sx/2;
    }else{
        mr=sy/2;
    }
    vector<int> ml= clipVector(_ml,-mr,mr);
    
    float thete;
    thete = (float)nowframe/maxframe*PI*2;
    for(int y=-mr; y<mr;y++){
        for(int x=-mr; x<mr;x++){
            int xx=sx/2+x; int yy=sy/2+y;
            float l=(float)sqrt(x*x+y*y);
            float ld=max(0.0f,min(1.0f,1.0f-(l/mr)));
            float offset_x=ml[0]*cos(thete)*ld; float offset_y=ml[1]*cos(thete)*ld;
            int targetX=(int)(xx+offset_x); int targetY=(int)(yy+offset_y);
            bool check=false;
            if(0<=targetX && targetX<sx){
                if(0<=targetY && targetY<sy){
                    for (int k = 0; k < shape[2]; k++){
                        *result.mutable_data(yy, xx, k)=*image.data(targetY, targetX, k);
                    }
                    check=true;
                }
            }
            if(check==false){
                for (int k = 0; k < shape[2]; k++){
                    *result.mutable_data(yy, xx, k)=0;
                }
            }
        }
    }
    return result;
}

template <typename T>//渡された範囲の画像(正方形のみ)の中心を画像サイズの小さい値をmrにしてゆらす0(入力、出力はmr*2とmr*2の正方形)
auto MakeGif(py::array_t<T> image){
    
    return 0;
}

PYBIND11_MODULE(CPictureModifier, m) {
	m.def("SquareCenterShake", &SquareCenterShake<uint8_t>,"");
}