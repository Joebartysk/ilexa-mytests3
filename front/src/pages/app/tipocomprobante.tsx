import { CONFIG } from 'src/config-global';

import { TipoComprobanteView } from 'src/sections/app-sections/tipocomprobante/view';

// ----------------------------------------------------------------------

export default function Page() {
	return (
		<>
			<title>{`Tipo Comprobante - ${CONFIG.appName}`}</title>

			<TipoComprobanteView />
		</>
	);
}
