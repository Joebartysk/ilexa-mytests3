import { CONFIG } from 'src/config-global';

import { PeriodicidadView } from 'src/sections/app-sections/periodicidad/view';

// ----------------------------------------------------------------------

export default function Page() {
	return (
		<>
			<title>{`Periodicidad - ${CONFIG.appName}`}</title>

			<PeriodicidadView />
		</>
	);
}
