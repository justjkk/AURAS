def parse_reg_nos(reg_str): # Format: 31107104001..117,301..314,404
   reg_index = []
   buff = ""
   for reg_range in [s.strip() for s in reg_str.split(',')]:
      if len(reg_range.split('..')) == 2: # Range
         reg_limits = [s.strip() for s in reg_range.split('..')]
         buff = buff[:-len(reg_limits[0])] + reg_limits[0]
         lower_no = int(buff)
         buff = buff[:-len(reg_limits[1])] + reg_limits[1]
         upper_no = int(buff)
         reg_index += range(lower_no, upper_no + 1)
      else: # Single number
         buff = buff[:-len(reg_range)] + reg_range
         reg_index += [int(buff)]
   return reg_index
