import schemdraw
import schemdraw.elements as elm

def gerar_svg_circuito(rc, xm, req, xeq):
    with schemdraw.Drawing(show=False) as d:
        d.config(unit=2.6, fontsize=11)

        # Entrada superior -> Nó do ramo paralelo
        d += elm.Dot(open=True).label('V1', loc='left')
        d += elm.Line().right().length(1.2)
        no_sup = d.here

        # Ramo paralelo esquerdo: Rc
        d += elm.Line().left().length(0.8)
        d += elm.Resistor().down().label(f'Rc\n{rc:.2f} Ω', loc='top')
        d += elm.Line().right().length(0.8)
        no_inf = d.here

        # Ramo paralelo direito: jXm
        d.push()
        d.move_from(no_sup)
        d += elm.Line().right().length(0.8)
        d += elm.Inductor2().down().label(f'jXm\nj{xm:.2f} Ω', loc='bottom')
        d += elm.Line().left().length(0.8)
        d.pop()

        # Ramo série: Req + jXeq
        d.move_from(no_sup)
        d += elm.Line().right().length(1.5)
        d += elm.Resistor().right().label(f'Req\n{req:.2f} Ω', loc='top')
        d += elm.Inductor2().right().label(f'jXeq\nj{xeq:.2f} Ω', loc='top')
        d += elm.Line().right().length(1.2)
        d += elm.Dot(open=True).label('V2', loc='right')

        # Barra inferior comum
        d.move_from(no_inf)
        d += elm.Line().left().length(1.2)
        d += elm.Dot(open=True)
        d.move_from(no_inf)
        d += elm.Line().right().length(7.7)
        d += elm.Dot(open=True)
        return d.get_imagedata('svg')