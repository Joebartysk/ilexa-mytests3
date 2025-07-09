import { CONFIG } from 'src/config-global';

import { BankStatementView } from 'src/sections/app-sections/bankstatement/view';

// ----------------------------------------------------------------------

export default function Page() {
	return (
		<>
			<title>{`Estados de Cuenta  - ${CONFIG.appName}`}</title>

			<BankStatementView />
		</>
	);
}
