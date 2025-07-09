import { CONFIG } from 'src/config-global';

import { TipofactorView } from 'src/sections/app-sections/tipofactor/view';

// ----------------------------------------------------------------------

export default function Page() {
	return (
		<>
			<title>{`Tipo Factor  - ${CONFIG.appName}`}</title>

			<TipofactorView />
		</>
	);
}
