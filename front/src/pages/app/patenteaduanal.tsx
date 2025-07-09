import { CONFIG } from 'src/config-global';

import { PatenteAduanalView } from 'src/sections/app-sections/patenteaduanal/view';

// ----------------------------------------------------------------------

export default function Page() {
	return (
		<>
			<title>{`Patente Aduanal  - ${CONFIG.appName}`}</title>

			<PatenteAduanalView />
		</>
	);
}
