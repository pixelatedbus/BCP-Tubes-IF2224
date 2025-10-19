program test3;
begin
  is_equal := 10 = 10;
  is_less := 5 < 10;
  is_not_equal := 5 <> 10;

  result_bool := is_equal and is_less;
  final_bool := is_not_equal or result_bool;
end.
