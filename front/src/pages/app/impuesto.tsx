import { CONFIG } from 'src/config-global';

import { ImpuestoView } from 'src/sections/app-sections/impuesto/view';

// ----------------------------------------------------------------------

export default function Page() {
	return (
		<>
			<title>{`Impuesto - ${CONFIG.appName}`}</title>

			<ImpuestoView />
		</>
	);
}
