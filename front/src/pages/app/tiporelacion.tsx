import { CONFIG } from 'src/config-global';

import { TipoRelacionView } from 'src/sections/app-sections/tiporelacion/view';

// ----------------------------------------------------------------------

export default function Page() {
	return (
		<>
			<title>{`Tipo Relación - ${CONFIG.appName}`}</title>

			<TipoRelacionView />
		</>
	);
}
