class Test < ActiveRecord::Migration
	def up
		create_table :test do |t|
			t.column :title, :string, :limit => 32, :null => false
			t.column :price, :float
			t.column :subject_id, :integer
			t.column :description, :text
			t.column :created_at, :timestamp
		end
	end

	def down
		drop_table :test
	end
end
