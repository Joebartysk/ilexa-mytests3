import { CONFIG } from 'src/config-global';

import { CpView } from 'src/sections/app-sections/cp/view';

// ----------------------------------------------------------------------

export default function Page() {
	return (
		<>
			<title>{`Codigo postal  - ${CONFIG.appName}`}</title>

			<CpView />
		</>
	);
}
