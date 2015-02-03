require 'standalone_migrations'
require 'foreigner'
StandaloneMigrations::Tasks.load_tasks
StandaloneMigrations.on_loaded do
	Foreigner.load
end
