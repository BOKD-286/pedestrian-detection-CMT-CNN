# Building docs script
# Requirements:
#   sudo apt-get install doxygen texlive ruby-dev
#   sudo gem install jekyll execjs therubyracer

if(NOT BUILD_docs OR NOT DOXYGEN_FOUND)
  return()
endif()

#################################################################################################
# Gather docs from <root>/examples/**/readme.md
function(gather_readmes_as_prebuild_cmd target gathered_dir root)
  set(full_gathered_dir ${root}/${gathered_dir})

  file(GLOB_RECURSE readmes ${root}/examples/readme.md ${root}/examples/README.md)
  foreach(file ${readmes})
    # Only use file if it is to be included in docs.
    file(STRINGS ${file} file_lines REGEX "include_in_docs: true")

    if(file_lines)
      # Since everything is called readme.md, rename it by its dirname.
      file(RELATIVE_PATH file ${root} ${file})
      get_filename_component(folder ${file} PATH)
      set(new_filename ${full_gathered_dir}/${folder}.md)

      # folder value might be like <subfolder>/readme.md. That's why make directory.
      get_filename_component(new_folder ${new_filename} PATH)
      add_custom_command(TARGET ${target} PRE_BUILD
        COMMAND ${CMAKE_COMMAND} -E make_directory ${new_folder}
        COMMAND ln -sf ${root}/${file} ${new_filename}
        COMMENT "Creating symlink ${new_filename} -> ${root}/${file}"
        WORKING_DIRECTORY ${root} VERBATIM)
    endif()
  endforeach()
endfunction()

################################################################################################
# Gather docs from examples/*.ipynb and add YAML front-matter.
function(gather_notebooks_as_prebuild_cmd target gathered_dir root)
  set(full_gathered_dir ${root}/${gathered_dir})

  if(NOT PYTHON_EXECUTABLE)
    message(STATUS "Python interpeter is not found. Can't include *.ipynb files in docs. Skipping...")
    return()
  endif()

  file(GLOB_RECURSE notebooks ${