import { CONFIG } from 'src/config-global';

import { RegimenFiscalView } from 'src/sections/app-sections/regimenfiscal/view';

// ----------------------------------------------------------------------

export default function Page() {
	return (
		<>
			<title>{`Regimen Fiscal - ${CONFIG.appName}`}</title>

			<RegimenFiscalView />
		</>
	);
}
