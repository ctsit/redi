#
# Collection of utility functions
# @author Andrei Sura

class Util

   # Static method for checking if a file exists
   def self.check_required_file(file_path)
      #path = File.expand_path("./#{name}", __FILE__)
      if !File.exists?(file_path)
         err = "Required file does not exist at path: #{file_path}"
         puts err
         raise err
      end
   end
end


