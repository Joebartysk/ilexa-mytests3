import { CONFIG } from 'src/config-global';

import { ExportacionView } from 'src/sections/app-sections/exportacion/view';

// ----------------------------------------------------------------------

export default function Page() {
	return (
		<>
			<title>{`Exportacion - ${CONFIG.appName}`}</title>

			<ExportacionView />
		</>
	);
}
