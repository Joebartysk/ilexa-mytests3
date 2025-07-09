import { CONFIG } from 'src/config-global';

import { ClaveunidadView } from 'src/sections/app-sections/claveunidad/view';

// ----------------------------------------------------------------------

export default function Page() {
	return (
		<>
			<title>{`Clave unidad  - ${CONFIG.appName}`}</title>

			<ClaveunidadView />
		</>
	);
}
