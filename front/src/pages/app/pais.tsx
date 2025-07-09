import { CONFIG } from 'src/config-global';

import { PaisView } from 'src/sections/app-sections/pais/view';

// ----------------------------------------------------------------------

export default function Page() {
	return (
		<>
			<title>{`Pais  - ${CONFIG.appName}`}</title>

			<PaisView />
		</>
	);
}
