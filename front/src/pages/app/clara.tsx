import { CONFIG } from 'src/config-global';

import { ClaraView } from 'src/sections/app-sections/clara/view';

// ----------------------------------------------------------------------

export default function Page() {
	return (
		<>
			<title>{`Estados de Cuenta-Clara  - ${CONFIG.appName}`}</title>

			<ClaraView />
		</>
	);
}
