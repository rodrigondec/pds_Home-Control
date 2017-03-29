﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace HomeControl.Domain.Potenciometro
{
    interface IPotenciometro
    {
        void aumentarValor();
        void diminuirValor();
        int getValorAtual();
        void diminuirParaValorMinimo();
        void aumentarParaValorMaximo();


    }
}