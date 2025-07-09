import { CONFIG } from 'src/config-global';

import { RegisterView } from 'src/sections/app-sections/register';

// ----------------------------------------------------------------------

export default function Page() {
	return (
		<>
			<title>{`Register - ${CONFIG.appName}`}</title>

			<RegisterView />
		</>
	);
}
