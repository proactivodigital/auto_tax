# Módulo de Impuestos Automáticos con UVT

## Descripción

Este módulo extiende la funcionalidad de los impuestos en Odoo añadiendo campos personalizados para gestionar el valor del **UVT** (Unidad de Valor Tributario) utilizado en los cálculos fiscales en Colombia. Permite aplicar impuestos basados en la cantidad de UVT tanto a nivel de **factura** como a nivel de **producto**.

### Funcionalidades

- Agrega un campo `tax_type` en el modelo `account.tax` para diferenciar impuestos a nivel de **factura** o **producto**.
- Permite gestionar un campo `uvt_amount` en el modelo `account.tax` para especificar el monto mínimo en UVT para cada tipo de impuesto.
- Permite configurar el valor de UVT a nivel de la empresa a través de los **ajustes de configuración**.

## ¿Cómo funciona?

El módulo permite gestionar los impuestos de la siguiente manera:

1. **A nivel de Producto**: El impuesto se aplica si el valor de UVT del producto (calculado a partir de su precio) supera el valor mínimo en UVT configurado en el impuesto.
2. **A nivel de Factura**: Si el total de la factura, expresado en UVT, supera el valor configurado en el impuesto, este se aplica a toda la factura.

## Instalación

### Pasos para instalar el módulo en Odoo.sh:

1. **Sube el módulo a tu instancia de Odoo.sh**:
    - Sube el módulo a tu repositorio en Odoo.sh, asegurándote de que esté en una carpeta adecuada dentro de tu estructura de módulos de Odoo.
   
2. **Instalar el módulo**:
    - Inicia sesión en tu instancia de Odoo.
    - Ve a **Aplicaciones** y haz clic en **Actualizar la lista de aplicaciones**.
    - Busca **"Account Tax automatically"**.
    - Haz clic en **Instalar**.

3. **Configura el módulo**:
    - Una vez instalado, ve a **Configuración** > **Contabilidad** > **Ajustes de la empresa**.
    - Aquí podrás definir el valor del **UVT** en el campo `Valor UVT`.
    
4. **Configura los impuestos**:
    - Ve a **Contabilidad** > **Impuestos**.
    - Aquí podrás configurar los impuestos y asignarles un **tipo** (factura o producto) y el **monto en UVT** necesario para que el impuesto se aplique.

## Campos Añadidos

- **Modelo `account.tax`**:
  - **`tax_type`**: Campo de selección para definir si el impuesto es aplicado a nivel de factura o producto.
  - **`uvt_amount`**: Monto en UVT necesario para aplicar el impuesto.
  
- **Modelo `res.company`**:
  - **`uvt_value_tax`**: Valor UVT utilizado en los cálculos fiscales de la empresa.

- **Modelo `res.config.settings`**:
  - **`uvt_value_tax`**: Valor UVT que se puede configurar a nivel de ajustes de la empresa.

## Dependencias

Este módulo depende de los siguientes módulos de Odoo:
- **base**: Base de datos de Odoo.
- **account**: Módulo de contabilidad de Odoo.
- **sale**: Módulo de ventas de Odoo.

## Licencia

Este módulo se distribuye bajo la licencia **LGPL-3**.