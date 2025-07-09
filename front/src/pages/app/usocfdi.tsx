import { CONFIG } from 'src/config-global';

import { UsoCfdiView } from 'src/sections/app-sections/usocfdi/view';

// ----------------------------------------------------------------------

export default function Page() {
	return (
		<>
			<title>{`Uso CFDI - ${CONFIG.appName}`}</title>

			<UsoCfdiView />
		</>
	);
}
